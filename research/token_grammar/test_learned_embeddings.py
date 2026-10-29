"""Tests S3.1B only on fabricated BTC-like returns. No API or private data."""
from dataclasses import replace
import math
import unittest

import numpy as np
import torch

from research.token_grammar.test_predictive import cases
from research.token_grammar.learned_embeddings import (
    CausalTokenProvider,TokenScalarModel,run_cases,VOCAB_SIZE,
)
from research.token_grammar.predictive import run_cases as decoded_s3a_run


class LearnedScalarTokensTests(unittest.TestCase):
    def test_token_ids_and_train_only_boundaries(self):
        train,dev=cases(2018),cases(2023)
        provider=CausalTokenProvider(train)
        initial=provider.quantile_boundaries_bps
        for name in ("signed_uniform_g1","signed_quantile_g2"):
            ids=provider.ids(dev,name)
            self.assertEqual(ids.shape,(40,20))
            self.assertEqual(ids.dtype,np.int64)
            self.assertTrue(np.all((ids>=0)&(ids<11)))
            vals=provider.decoded(dev,name)
            np.testing.assert_array_equal(
                vals,provider.centers(name)[ids])
            altered=[replace(c,target_usd=c.target_usd*1.7) for c in dev]
            np.testing.assert_array_equal(
                ids,provider.ids(altered,name))
            new_dev=[replace(c,continuous_past_bps=tuple(1e8 for _ in range(20)))
                     for c in dev]
            provider.ids(new_dev,name)
        self.assertEqual(initial,provider.quantile_boundaries_bps)

    def test_ordered_embedding_at_initialisation_exactly_matches_numeric(self):
        provider=CausalTokenProvider(cases(2018))
        for grammar in ("signed_uniform_g1","signed_quantile_g2"):
            tokens=provider.ids(cases(2023),grammar)
            centers=provider.centers(grammar)
            for mode in ("regression","joint"):
                torch.manual_seed(17)
                from research.continuous_direction.models import ContinuousDirectionModel
                ref=ContinuousDirectionModel(width=16,depth=1,mode=mode)
                torch.manual_seed(17)
                learn=TokenScalarModel(width=16,depth=1,mode=mode,
                    init_style="ordered",centers_bps=centers,scale_bps=5.)
                expected=torch.as_tensor(centers[tokens]/5.,dtype=torch.float64)
                got=torch.as_tensor(tokens,dtype=torch.int64)
                with torch.no_grad():
                    x1,y1=ref(expected)
                    x2,y2=learn(got)
                torch.testing.assert_close(x1,x2,rtol=1e-14,atol=1e-14)
                torch.testing.assert_close(y1,y2,rtol=1e-14,atol=1e-14)
                self.assertEqual(
                    learn.backbone_initial_sha256,
                    __import__("hashlib").sha256(b"".join(
                        p.detach().cpu().contiguous().numpy().tobytes()
                        for p in ref.parameters())).hexdigest())
                self.assertEqual(
                    sum(p.numel() for p in learn.parameters())
                    -sum(p.numel() for p in ref.parameters()),VOCAB_SIZE)

    def test_s3a_decoded_reproduced_and_random_vs_ordered_capacity(self):
        train,dev=cases(2018),cases(2023)
        opts=dict(interval="D1",widths=(16,),depths=(1,),
                  seeds=(11,),modes=("regression","joint"),steps=2)
        previous=decoded_s3a_run(train,dev,
            grammars=("signed_uniform_g1","signed_quantile_g2"),**opts)
        report=run_cases(train,dev,**opts)
        self.assertFalse(report["labels_2026_opened"])
        self.assertFalse(report["independent_test_used"])
        self.assertFalse(report["learned_vs_decoded_trainable_params_matched"])
        self.assertTrue(report["ordered_vs_random_trainable_params_matched"])
        self.assertEqual(len(report["results"]),12)
        for mode in ("regression","joint"):
            for grammar in ("signed_uniform_g1","signed_quantile_g2"):
                old=next(x for x in previous["results"] if x["mode"]==mode
                         and x["representation"]==grammar)
                rows={r["arm"]:r for r in report["results"]
                      if r["mode"]==mode and r["grammar"]==grammar}
                fixed=rows["decoded"]
                for m in ("balanced_direction_accuracy","direction_accuracy_all",
                          "mae_native_usd","mae_bps_anchor",
                          "absolute_magnitude_error_bps"):
                    self.assertAlmostEqual(fixed[m],old[m],places=10,msg=m)
                self.assertEqual(len({r["backbone_initial_sha256"]
                        for r in rows.values()}),1)
                self.assertEqual(rows["decoded"]["embedding_trainable_parameters"],0)
                self.assertEqual(rows["embedding_ordered"]["embedding_trainable_parameters"],11)
                self.assertEqual(rows["embedding_random"]["embedding_trainable_parameters"],11)
                self.assertEqual(rows["embedding_ordered"]["parameter_count"],
                                 rows["embedding_random"]["parameter_count"])
                self.assertEqual(rows["embedding_ordered"]["parameter_count"]
                                 -fixed["parameter_count"],11)
                if mode=="joint":
                    self.assertTrue(all(r["binary_probabilities_from_trained_head"]
                                        for r in rows.values()))
                else:
                    self.assertTrue(all(r["brier_skill_vs_train_prior"] is None
                                        for r in rows.values()))
        self.assertTrue(all(math.isfinite(r["mae_bps_anchor"])
                            for r in report["results"]))

    def test_future_year_forbidden_and_bad_ids_rejected(self):
        with self.assertRaises(ValueError):
            run_cases(cases(2018),cases(2026),
                interval="M1",widths=(16,),depths=(1,),
                seeds=(7,),steps=1)
        provider=CausalTokenProvider(cases(2018))
        torch.manual_seed(5)
        model=TokenScalarModel(width=16,depth=1,mode="joint",
            init_style="ordered",
            centers_bps=provider.centers("signed_uniform_g1"),
            scale_bps=5.)
        with self.assertRaises(ValueError):
            model(torch.full((2,20),11,dtype=torch.int64))
        with self.assertRaises(ValueError):
            model(torch.ones((2,20),dtype=torch.float64))
        with self.assertRaises(ValueError):
            provider.ids([replace(cases(2023)[0],continuous_past_bps=(1.,))],
                         "signed_quantile_g2")


if __name__=="__main__":
    unittest.main()
