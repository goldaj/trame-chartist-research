"""S2 adversarial tests using manufactured returns ONLY."""
from datetime import datetime,timedelta,timezone
import math
import unittest

import numpy as np
import torch

from research.btc_h1_m1.stream import Case
from research.continuous_direction.models import (
    ContinuousDirectionModel,forecast_prices,
)
from research.continuous_direction.runner import run_cases


def fabricated_case(year,index):
    stamp=datetime(year,1,1,tzinfo=timezone.utc)+timedelta(hours=index)
    previous_price=100+index*.01
    # Tiny nonzero returns would have integer codec zero.
    move_bps=(0.2 if index%3==0 else -0.1 if index%3==1 else 0.0)
    target=previous_price*math.exp(move_bps/10000)
    return Case(
        origin_open=stamp-timedelta(hours=1),
        target_open=stamp,
        decision_time=stamp,
        label_available_time=stamp+timedelta(hours=1),
        encoded_past=tuple(0 for _ in range(20)),
        encoded_target=0,
        anchor_usd=previous_price,
        target_usd=target,
        grade="fake",
        continuous_past_bps=tuple((index+i)%3*.25-.25 for i in range(20)),
    )


class S2Tests(unittest.TestCase):
    def test_discrete_zero_can_mask_true_direction(self):
        c=fabricated_case(2018,0)
        self.assertEqual(c.encoded_target,0)
        self.assertGreater(c.target_usd,c.anchor_usd)
        self.assertTrue(any(v!=0 for v in c.continuous_past_bps))

    def test_causal_no_future_token_leak_and_finite_gradients(self):
        torch.manual_seed(7)
        torch.set_num_threads(1)
        x=torch.randn(2,6,dtype=torch.float64)
        changed=x.clone()
        changed[:,-1]=99
        for depth in (1,2):
            model=ContinuousDirectionModel(width=16,depth=depth,mode="joint")
            with torch.no_grad():
                a=model.input_proj(x.unsqueeze(-1))
                b=model.input_proj(changed.unsqueeze(-1))
                for block in model.blocks:
                    a=block(a)
                    b=block(b)
                torch.testing.assert_close(
                    a[:,:-1],b[:,:-1],atol=1e-10,rtol=1e-10)
            y=torch.as_tensor([.1,-.2],dtype=torch.float64)
            loss=model.loss(x,y)
            self.assertTrue(bool(torch.isfinite(loss)))
            loss.backward()
            self.assertTrue(all(p.grad is None or bool(torch.isfinite(p.grad).all())
                                for p in model.parameters()))

    def test_joint_forces_forecast_sign_consistent_with_classifier(self):
        data=torch.zeros((2,20),dtype=torch.float64)
        anchors=np.array([100.,110.])
        for mode in ("joint","regression"):
            model=ContinuousDirectionModel(width=16,mode=mode)
            with torch.no_grad():
                model.return_head.weight.zero_()
                model.return_head.bias.fill_(.5)
                model.direction_head.weight.zero_()
                model.direction_head.bias.fill_(-5)
            predicted,p_up,_=forecast_prices(
                model,data,anchors,scale_bps=10.0)
            self.assertTrue(np.all(p_up<.5))
            if mode=="joint":
                self.assertTrue(np.all(predicted<anchors))
            else:
                self.assertTrue(np.all(predicted>anchors))

    def test_two_modes_replay_same_fixture_without_2026(self):
        train=[fabricated_case(2018,i) for i in range(40)]
        dev=[fabricated_case(2023,i) for i in range(40)]
        result=run_cases(train,dev,interval="M1",widths=(16,),depths=(1,),
                         modes=("regression","joint"),steps=2,seeds=(7,),
                         data_origin="ARTIFICIAL_FIXTURE")
        self.assertEqual(len(result["results"]),2)
        self.assertTrue(result["train_only_normalization"])
        self.assertFalse(result["labels_2026_opened"])
        self.assertEqual(result["quantized_target_zero_fraction_dev"],1.)
        self.assertLess(result["true_target_flat_fraction_dev"],1.)
        for r in result["results"]:
            self.assertTrue(math.isfinite(r["mae_bps_anchor"]))
            self.assertTrue(math.isfinite(r["absolute_magnitude_error_bps"]))
        with self.assertRaises(ValueError):
            run_cases(train,[fabricated_case(2026,i) for i in range(40)],
                      interval="M1",widths=(16,),depths=(1,),
                      modes=("joint",),steps=1,seeds=(7,))

if __name__=="__main__":
    unittest.main()
