"""Constructed numerical counterexamples, not market observations."""
import math
import unittest

import numpy as np
from scipy.stats import norm

try:
    from .head import (A, GRID, Head, decode_lattice_price,
                       hierarchical_logits, log_rounded_normal_mass)
except ImportError:
    from head import (A, GRID, Head, decode_lattice_price,
                      hierarchical_logits, log_rounded_normal_mass)


class HeadNumericsTests(unittest.TestCase):
    def test_proposal_initialization_normalized(self):
        h = Head()
        self.assertAlmostEqual(h.log_z, 0, delta=1e-12)
        self.assertAlmostEqual(h.mass_audit()['sum'], 1, delta=1e-12)
        self.assertAlmostEqual(math.exp(h.log_prob(0)),
                               norm.cdf(.5/8)-norm.cdf(-.5/8), delta=1e-12)

    def test_positive_tail_no_cdf_cancellation(self):
        h = Head(mu=0, sigma=8)
        self.assertTrue(math.isfinite(h.log_prob(2000)))
        self.assertLess(h.log_prob(2000), -1000)
        self.assertTrue(math.isfinite(h.log_prob(-2000)))
        self.assertAlmostEqual(h.log_prob(2000), h.log_prob(-2000), delta=1e-6)

    def test_gaussian_interval_matches_independent_integral(self):
        from scipy.integrate import quad
        for k, mu, sd in [(0,0,8),(24,0,8),(-13,1,4),(7,3,0.25)]:
            with self.subTest((k,mu,sd)):
                lo,hi=(k-.5-mu)/sd,(k+.5-mu)/sd
                integral=quad(lambda z: math.exp(-z*z/2)/math.sqrt(2*math.pi),lo,hi)[0]
                self.assertAlmostEqual(math.exp(log_rounded_normal_mass(k,mu,sd)),
                                       integral, delta=1e-12)

    def test_correction_is_normalized_even_in_saturated_cases(self):
        arr = np.zeros(4096)
        arr[2048] = 20.0
        arr[2049] = -20.0
        for mu,s,S in [(0,8,64), (256,64,64), (-256,64,64),
                       (256,256,256), (0,.25,64)]:
            with self.subTest((mu,s,S)):
                h=Head(mu,s,logits=arr,max_sigma=float(S))
                self.assertAlmostEqual(h.mass_audit()['sum'],1,delta=5e-13)
                self.assertTrue(math.isfinite(h.negative_log_likelihood(-4000)))
                self.assertTrue(math.isfinite(h.negative_log_likelihood(4000)))
                self.assertLessEqual(float(np.max(np.abs(h.correction))),A)

    def test_flat_matches_hier_when_logit_values_identical(self):
        coarse = np.sin(np.arange(512)/53)
        bits = np.array([[.5,-.5],[-.4,.4],[.3,-.3]])
        g = hierarchical_logits(coarse,bits)
        flat = Head(logits=g)
        hier = Head(logits=hierarchical_logits(coarse,bits))
        self.assertEqual(g.shape,(4096,))
        for k in [-2048,-2047,-1,0,1,2047,2500]:
            self.assertAlmostEqual(flat.log_prob(k),hier.log_prob(k),delta=1e-14)
        self.assertAlmostEqual(flat.log_z,hier.log_z,delta=1e-14)

    def test_hier_negative_integer_decomposition(self):
        c = np.arange(512,dtype=float)
        bits = np.array([[0,1],[0,2],[0,4]],dtype=float)
        g=hierarchical_logits(c,bits)
        self.assertEqual(g[-1 + 2048],255+7)
        self.assertEqual(g[-8 + 2048],255)
        self.assertEqual(g[-9 + 2048],254+7)

    def test_grad_logits_finite_difference_for_positive_and_negative_target(self):
        g=np.zeros(4096)
        g[2048]=1.3
        g[2049]=-0.7
        g[2047]=0.2
        for target in (0,1,4000):
            h=Head(logits=g)
            gradient=h.grad_logits(target)
            for ix in (2047,2048,2049):
                eps=1e-5
                gp, gm=g.copy(),g.copy()
                gp[ix]+=eps;gm[ix]-=eps
                # In an ultra-rare tail NLL can be huge; subtracting two
                # near-equal losses destroys finite-difference precision.
                # Differentiate logZ separately and add target correction.
                numeric=(Head(logits=gp).log_z-Head(logits=gm).log_z)/(2*eps)
                if target == ix - 2048:
                    numeric -= (1.0 - np.tanh(g[ix]/A)**2)
                self.assertAlmostEqual(gradient[ix],numeric,delta=4e-9)

    def test_pmf_empirical_sampling(self):
        h=Head()
        rng=np.random.default_rng(17)
        samples=np.array([h.sample(rng) for _ in range(1200)])
        self.assertLess(abs(float(np.mean(samples))),1)
        self.assertLess(abs(float(np.std(samples))-8),1)

    def test_price_decode_exact_cumulative_state_and_overflow(self):
        self.assertAlmostEqual(decode_lattice_price(100,0.08,10),
                               100*math.exp(.1), delta=1e-12)
        with self.assertRaises(OverflowError):
            decode_lattice_price(1,1,10000000)
        with self.assertRaises(ValueError):
            decode_lattice_price(0,1,1)

    def test_reject_proposals_that_exceed_predeclared_bounds(self):
        for kwargs in ({'mu':300}, {'sigma':257}, {'sigma':0},
                       {'sigma':.1}, {'sigma':float('nan')},
                       {'max_sigma':80}, {'logits':np.zeros(5)}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                Head(**kwargs)


if __name__ == '__main__':
    unittest.main()


class ConstructedTrainingFixtureTests(unittest.TestCase):
    def test_corrections_fit_declared_bimodal_fixture(self):
        try:
            from synthetic_fit import run
        except ImportError:
            from .synthetic_fit import run
        report=run()
        scores=report['scores']
        self.assertLess(scores['FLAT']['test_nll'], scores['BASE']['test_nll'])
        self.assertLess(scores['HIER']['test_nll'], scores['BASE']['test_nll'])
        self.assertFalse(report['market_data_read'])
        self.assertFalse(report['trained_gpt'])


class CausalPathTests(unittest.TestCase):
    def test_path_inputs_are_only_prior_generated_states(self):
        try:
            from rollout import rollout
        except ImportError:
            from .rollout import rollout
        seen=[]
        def policy(h, previous):
            seen.append((h,previous))
            return Head()
        path=rollout(100.,.05,policy,np.random.default_rng(10))
        self.assertEqual(len(path.prices),20)
        self.assertEqual(seen[0],(1,0))
        self.assertEqual([old for _,old in seen[1:]],list(path.cumulative_codes[:-1]))
        self.assertEqual(tuple(np.cumsum(path.codes)),path.cumulative_codes)
        self.assertTrue(all(math.isfinite(p) and p>0 for p in path.prices))

    def test_teacher_forcing_uses_realized_codes_only_after_scoring(self):
        try:
            from rollout import teacher_forced_log_likelihood
        except ImportError:
            from .rollout import teacher_forced_log_likelihood
        observed=[]
        def policy(h, prev):
            observed.append((h, prev))
            return Head()
        loglik=teacher_forced_log_likelihood([3, -2, 4],policy)
        self.assertEqual(observed,[(1,0),(2,3),(3,1)])
        self.assertAlmostEqual(loglik,sum(Head().log_prob(k) for k in (3,-2,4)))

    def test_empirical_crps_matches_pairwise_definition(self):
        try:
            from rollout import empirical_crps
        except ImportError:
            from .rollout import empirical_crps
        def brute(vals,y):
            n=len(vals)
            return (sum(abs(v-y) for v in vals)/n -
                    sum(abs(a-b) for a in vals for b in vals)/(2*n*n))
        for values,y in [([1,3],2),([1,2,4],3),([4],2),([99,101,150],102)]:
            self.assertAlmostEqual(empirical_crps(values,y),brute(values,y),delta=1e-11)
        with self.assertRaises(ValueError):
            empirical_crps([float('nan')],100.)
        with self.assertRaises(ValueError):
            empirical_crps([],100.)
