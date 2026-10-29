"""Stage-2.1 to 2.3: synthetic independence and causal-mask invariants."""
import unittest
import numpy as np
import torch

try:
    from .data import generated_codes, previous_codes, get_split, oracle_mu
    from .model import MiniTRAME
except ImportError:
    from data import generated_codes, previous_codes, get_split, oracle_mu
    from model import MiniTRAME


class SyntheticDataAndModelTests(unittest.TestCase):
    def test_distinct_seed_streams_and_protected_reserved_test(self):
        a=get_split('train')
        dev=get_split('development')
        self.assertEqual(a.shape,(192,20))
        self.assertEqual(dev.shape,(96,20))
        self.assertFalse(np.array_equal(a[:96],dev))
        with self.assertRaises(PermissionError):
            get_split('reserved_synthetic_test')

    def test_generator_reproducible_and_shift_strictly_past(self):
        a=generated_codes(10,seed=42)
        self.assertTrue(np.array_equal(a,generated_codes(10,seed=42)))
        prev=previous_codes(a)
        self.assertTrue(np.all(prev[:,0]==0))
        self.assertTrue(np.array_equal(prev[:,1:],a[:,:-1]))
        self.assertTrue(np.allclose(oracle_mu(prev),.75*prev))

    def test_causal_transformer_mask_disallows_future_inputs(self):
        torch.manual_seed(44)
        net=MiniTRAME(width=16).eval()
        previous=previous_codes(generated_codes(3,seed=1))
        a=torch.tensor(previous,dtype=torch.float64)
        b=a.clone()
        b[:,10:] += 10000.  # perturb strictly later inputs
        with torch.no_grad():
            ma,sa=net(a)
            mb,sb=net(b)
        torch.testing.assert_close(ma[:,:10],mb[:,:10],atol=1e-11,rtol=1e-11)
        torch.testing.assert_close(sa[:,:10],sb[:,:10],atol=1e-11,rtol=1e-11)

    def test_one_backward_step_updates_real_parameters(self):
        torch.manual_seed(77)
        net=MiniTRAME().train()
        labels=generated_codes(8,seed=19)
        prior=torch.tensor(previous_codes(labels),dtype=torch.float64)
        targets=torch.tensor(labels,dtype=torch.float64)
        optim=torch.optim.AdamW(net.parameters(),lr=.003)
        before=net.output.weight.detach().clone()
        loss=net.nll(prior,targets)
        self.assertTrue(torch.isfinite(loss))
        optim.zero_grad()
        loss.backward()
        self.assertTrue(all(p.grad is not None and torch.isfinite(p.grad).all() for p in net.parameters()))
        optim.step()
        self.assertGreater(float((net.output.weight.detach()-before).abs().max()),0.)


if __name__=='__main__':
    unittest.main()
