"""Independent PyTorch / SciPy checks, all values constructed."""
import math
import unittest

import numpy as np
import torch

try:
    from .head import Head
    from .torch_head import nll, bounds_transform, logit_for_sigma
except ImportError:
    from head import Head
    from torch_head import nll, bounds_transform, logit_for_sigma


class TorchHeadTests(unittest.TestCase):
    def test_candidate_initialization_and_symmetry(self):
        rawmu=torch.tensor(0.,dtype=torch.float64,requires_grad=True)
        rawsig=torch.tensor(logit_for_sigma(8.),dtype=torch.float64,requires_grad=True)
        mu,sigma=bounds_transform(rawmu,rawsig)
        self.assertAlmostEqual(float(mu),0,delta=1e-12)
        self.assertAlmostEqual(float(sigma),8,delta=1e-12)
        self.assertAlmostEqual(float(nll(0,mu,sigma)[0]),
                               Head().negative_log_likelihood(0),delta=1e-11)
        nll(0,mu,sigma)[0].backward()
        self.assertTrue(math.isfinite(float(rawmu.grad)))
        self.assertTrue(math.isfinite(float(rawsig.grad)))

    def test_mu_sigma_gradient_against_scipy_centered_differences(self):
        # Finite differences performed in SciPy (independent implementation).
        # Avoid parameter boundaries and NLL subtraction in deeply rare cells.
        cases=[(0.,8.,0),(3.,12.,37),(-210.,60.,4000),(120.,60.,-4000),
               (0.,.30,0),(8.,1.,8)]
        for center, spread, target in cases:
            with self.subTest(mu=center,sigma=spread,target=target):
                mu=torch.tensor(center,dtype=torch.float64,requires_grad=True)
                sig=torch.tensor(spread,dtype=torch.float64,requires_grad=True)
                loss, logz=nll(target,mu,sig)
                self.assertTrue(math.isfinite(float(loss)))
                loss.backward()
                steps=[1e-4,1e-4]
                for component, step, analytic in (
                        ('mu',steps[0],float(mu.grad)),
                        ('sigma',steps[1],float(sig.grad))):
                    def evaluate(delta):
                        p=center+(delta if component=='mu' else 0.)
                        s=spread+(delta if component=='sigma' else 0.)
                        return Head(p,s,max_sigma=64.).negative_log_likelihood(target)
                    # Differentiate loss on a finite cell; the relevant
                    # rounded Gaussian code can be astronomically unlikely.
                    approx=(evaluate(step)-evaluate(-step))/(2*step)
                    self.assertTrue(math.isfinite(approx))
                    self.assertAlmostEqual(analytic,approx,
                        delta=max(2e-4,abs(analytic)*1e-4))

    def test_corrected_distribution_logz_and_gradient(self):
        rng=np.random.default_rng(20261025)
        correction=torch.tensor(rng.normal(0,.5,4096),
                                dtype=torch.float64,requires_grad=True)
        mu=torch.tensor(2.,dtype=torch.float64,requires_grad=True)
        sigma=torch.tensor(7.,dtype=torch.float64,requires_grad=True)
        loss,z=nll(17,mu,sigma,correction)
        ref=Head(2.,7.,logits=correction.detach().numpy(),max_sigma=64.)
        self.assertAlmostEqual(float(z),ref.log_z,delta=3e-11)
        self.assertAlmostEqual(float(loss),ref.negative_log_likelihood(17),delta=3e-11)
        loss.backward()
        self.assertTrue(torch.isfinite(correction.grad).all())
        self.assertTrue(torch.isfinite(mu.grad))
        self.assertTrue(torch.isfinite(sigma.grad))
        for index in (2048,2065):
            self.assertAlmostEqual(float(correction.grad[index]),
                                   ref.grad_logits(17)[index],delta=3e-10)

    def test_non_finite_and_dtype_refused(self):
        with self.assertRaises(TypeError):
            nll(1,torch.tensor(0.,dtype=torch.float32),
                torch.tensor(8.,dtype=torch.float32))
        with self.assertRaises(ValueError):
            nll(1,torch.tensor(0.,dtype=torch.float64),
                torch.tensor(-1.,dtype=torch.float64))

    def test_boundary_saturation_is_explicit_not_hidden(self):
        rawmu=torch.tensor(4096.,dtype=torch.float64,requires_grad=True)
        rawsig=torch.tensor(40.,dtype=torch.float64,requires_grad=True)
        mu,sigma=bounds_transform(rawmu,rawsig)
        self.assertLessEqual(float(mu),256.)
        self.assertLessEqual(float(sigma),64.)
        # These gradients saturate; do not mistake finiteness for trainability.
        (mu + sigma).backward()
        self.assertLess(abs(float(rawmu.grad)),1e-10)
        self.assertLess(abs(float(rawsig.grad)),1e-10)


if __name__=='__main__':
    unittest.main()
