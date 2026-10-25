"""Finite and causally masked P1-B0 corrections on artificial paths."""
import math
import unittest
import numpy as np
import torch

from research.mini_gpt_synthetic.data import generated_codes, previous_codes
from research.mini_gpt_synthetic.corrected_model import (CorrectedMiniTRAME,
                                                          corrected_batched_nll)
from research.mini_gpt_synthetic.model import MiniTRAME


class CorrectedModelTests(unittest.TestCase):
    def test_hier_flat_agree_at_zero_corrections_even_for_rare_code(self):
        mu=torch.tensor([[0.]],dtype=torch.float64)
        sigma=torch.tensor([[8.]],dtype=torch.float64)
        target=torch.tensor([[4000.]],dtype=torch.float64)
        zeros=torch.zeros((1,1,4096),dtype=torch.float64)
        result=corrected_batched_nll(target,mu,sigma,zeros)
        self.assertTrue(math.isfinite(float(result)))
        self.assertGreater(float(result),1e5)

    def test_full_corrected_model_autograd_and_causality(self):
        codes=generated_codes(3,seed=987,length=8)
        prior=torch.tensor(previous_codes(codes),dtype=torch.float64)
        future_mutated=prior.clone()
        future_mutated[:,4:]+=10000
        target=torch.tensor(codes,dtype=torch.float64)
        for arm in ['HIER','FLAT']:
            with self.subTest(arm=arm):
                torch.manual_seed(5)
                model=CorrectedMiniTRAME(arm,length=8)
                model.eval()
                with torch.no_grad():
                    m1,s1,c1=model.forward_full(prior)
                    m2,s2,c2=model.forward_full(future_mutated)
                    torch.testing.assert_close(m1[:,:4],m2[:,:4],atol=1e-11,rtol=1e-11)
                    torch.testing.assert_close(s1[:,:4],s2[:,:4],atol=1e-11,rtol=1e-11)
                    torch.testing.assert_close(c1[:,:4],c2[:,:4],atol=1e-11,rtol=1e-11)
                loss=model.nll(prior,target)
                self.assertTrue(torch.isfinite(loss))
                loss.backward()
                self.assertTrue(all(p.grad is not None and
                           torch.isfinite(p.grad).all() for p in model.parameters()))

    def test_corrected_zero_initialization_equals_base_from_same_backbone(self):
        codes=generated_codes(2,seed=123,length=8)
        prior=torch.tensor(previous_codes(codes),dtype=torch.float64)
        target=torch.tensor(codes,dtype=torch.float64)
        torch.manual_seed(42)
        base=MiniTRAME(length=8)
        torch.manual_seed(42)
        hier=CorrectedMiniTRAME('HIER',length=8)
        torch.manual_seed(42)
        flat=CorrectedMiniTRAME('FLAT',length=8)
        with torch.no_grad():
            b=float(base.nll(prior,target))
            h=float(hier.nll(prior,target))
            f=float(flat.nll(prior,target))
        self.assertAlmostEqual(b,h,delta=1e-9)
        self.assertAlmostEqual(b,f,delta=1e-9)


if __name__=='__main__':
    unittest.main()
