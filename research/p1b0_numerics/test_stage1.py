"""Synthetic invariants for P1-B0 rare events and causal 20-step forecasts."""
import math
import unittest

import numpy as np

try:
    from .head import Head
    from .tails import conditional_tail_sample, log_tail_probability, sampling_support_audit
    from .rollout import rollout, teacher_forced_log_likelihood, empirical_crps
except ImportError:
    from head import Head
    from tails import conditional_tail_sample, log_tail_probability, sampling_support_audit
    from rollout import rollout, teacher_forced_log_likelihood, empirical_crps


class TailAndCausalityTests(unittest.TestCase):
    def test_tail_underflow_identified_without_forgetting_log_mass(self):
        h=Head(mu=0.,sigma=8.,max_sigma=64.)
        audit=sampling_support_audit(h)
        self.assertTrue(audit['left_underflow'])
        self.assertTrue(audit['right_underflow'])
        self.assertLess(audit['left_logp'],-10000)
        self.assertTrue(math.isfinite(audit['left_logp']))
        self.assertFalse(audit['unconditional_extreme_sampling_certified'])

    def test_conditional_tail_stress_sampling_far_beyond_double_underflow(self):
        h=Head(mu=0.,sigma=8.,max_sigma=64.)
        rng=np.random.default_rng(20261025)
        left=[conditional_tail_sample(h,'left',rng) for _ in range(50)]
        right=[conditional_tail_sample(h,'right',rng) for _ in range(50)]
        self.assertTrue(all(k < -2048 for k in left))
        self.assertTrue(all(k > 2047 for k in right))
        self.assertEqual(len(left),50)
        self.assertEqual(len(right),50)

    def test_conditional_tail_not_misrepresented_as_unconditional(self):
        h=Head()
        self.assertLess(log_tail_probability(h,'left'),-700)
        self.assertEqual(sampling_support_audit(h)['left_float64_mass'],0)

    def test_rollout_replay_invariant_and_generated_state_only(self):
        def policy(step, state):
            self.assertIsInstance(step,int)
            self.assertIsInstance(state,int)
            self.assertTrue(1 <= step <= 20)
            return Head(mu=max(-30,min(30,state/5)),sigma=8.,max_sigma=64.)
        result1=rollout(123.,.02,policy,np.random.default_rng(20261025))
        result2=rollout(123.,.02,policy,np.random.default_rng(20261025))
        self.assertEqual(result1,result2)
        self.assertEqual(tuple(np.cumsum(result1.codes)),result1.cumulative_codes)
        self.assertEqual(len(result1.codes),20)
        self.assertTrue(all(x>0 and math.isfinite(x) for x in result1.prices))

    def test_causal_teacher_forcing_future_not_passed_in(self):
        seen=[]
        def policy(step, previous):
            seen.append((step,previous))
            return Head(mu=max(-30,min(30,previous/5.)),sigma=8.,max_sigma=64.)
        ll=teacher_forced_log_likelihood([1,-1,7,-5],policy)
        self.assertEqual(seen,[(1,0),(2,1),(3,0),(4,7)])
        self.assertTrue(math.isfinite(ll))

    def test_empirical_crps_nonnegative_permutation_and_scale(self):
        x=np.array([60.,150.,80.,100.,110.,170.])
        y=95.
        score=empirical_crps(x,y)
        self.assertGreaterEqual(score,0.)
        self.assertAlmostEqual(score,empirical_crps(x[::-1],y),delta=1e-10)
        self.assertAlmostEqual(score*100.,empirical_crps(x*100.,y*100.),delta=1e-9)
        self.assertAlmostEqual(empirical_crps([y],y),0.,delta=1e-12)


if __name__=='__main__':
    unittest.main()
