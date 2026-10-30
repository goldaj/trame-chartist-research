"""S3.1B true embedding, identical architecture, anti-leakage synthetic tests."""
from dataclasses import replace
import math
import unittest

import numpy as np
import torch

from research.token_grammar.test_predictive import cases
from research.token_grammar.token_embeddings import (
    ARMS,VOCAB_SIZE,TokenHybridDirectionModel,EmbeddingGrammarFeatures,
)
from research.token_grammar.embedding_runner import run_cases


class EmbeddingResearchTests(unittest.TestCase):
    def test_embedding_receives_actual_gradients(self):
        torch.manual_seed(7)
        model=TokenHybridDirectionModel(
            width=16,depth=1,mode="joint")
        x=torch.zeros((3,20,2),dtype=torch.float64)
        x[0,:,1]=1.0
        x[1,:,1]=6.0
        x[2,:,1]=2.0
        y=torch.tensor([.4,-.7,.1],dtype=torch.float64)
        loss=model.loss(x,y)
        loss.backward()
        grad=model.token_embedding.weight.grad
        self.assertIsNotNone(grad)
        self.assertGreater(float(grad[1].abs().sum()),0.0)
        self.assertGreater(float(grad[6].abs().sum()),0.0)
        self.assertGreater(float(grad[2].abs().sum()),0.0)
        self.assertEqual(float(grad[10].abs().sum()),0.0)

    def test_g2_train_only_and_embeddings_never_observe_dev_labels(self):
        train,dev=cases(2018),cases(2023)
        codec=EmbeddingGrammarFeatures(train)
        thresholds=codec.quantile_boundaries_bps
        original={a:codec(dev,a) for a in ARMS}
        altered=[replace(c,target_usd=c.target_usd*1.3,
                         encoded_target=111) for c in dev]
        for a in ARMS:
            np.testing.assert_array_equal(original[a],codec(altered,a))
        self.assertEqual(thresholds,codec.quantile_boundaries_bps)
        for a in ("g1_learned_token","g2_learned_token"):
            self.assertTrue(np.all(original[a][:,:,0]==0))
            self.assertTrue(np.all(np.floor(original[a][:,:,1])
                                   ==original[a][:,:,1]))
            self.assertTrue(np.all((original[a][:,:,1]>=0)
                                   &(original[a][:,:,1]<VOCAB_SIZE)))
        self.assertTrue(np.any(original["continuous_scalar"][:,:,0]!=0))
        self.assertTrue(np.all(original["continuous_scalar"][:,:,1]==0))

    def test_reject_fractional_out_of_vocab_tokens(self):
        model=TokenHybridDirectionModel(width=16,depth=1)
        x=torch.zeros((2,20,2),dtype=torch.float64)
        for bad in (-1,11,3.3,float("nan")):
            b=x.clone()
            b[0,0,1]=bad
            with self.subTest(token=bad),self.assertRaises(ValueError):
                model(b)

    def test_10_fits_paired_same_weights_and_no_holdout(self):
        train,dev=cases(2018),cases(2023)
        r=run_cases(train,dev,interval="D1",widths=(16,),
                    depths=(1,),seeds=(31,),steps=1)
        self.assertEqual(r["experiment"],"TRAME_S3_1B_TRUE_TOKEN_EMBEDDING_V1")
        self.assertEqual(len(r["results"]),10)
        self.assertFalse(r["labels_2026_opened"])
        self.assertTrue(r["quantile_fit_on_train_only"])
        self.assertEqual(len({x["initial_state_sha256"] for x in r["results"]}),1)
        self.assertEqual(len({x["parameter_count"] for x in r["results"]}),1)
        self.assertEqual(len({x["train_only_continuous_scale_bps"] for x in r["results"]}),1)
        for row in r["results"]:
            self.assertTrue(row["trainable_embedding"])
            self.assertEqual(row["token_vocab_size"],11)
            self.assertTrue(math.isfinite(row["mae_bps_anchor"]))
            self.assertTrue(math.isfinite(row["absolute_magnitude_error_bps"]))
            if row["mode"]=="joint":
                self.assertIsInstance(row["brier_nonflat"],float)
            else:
                self.assertIsNone(row["brier_nonflat"])

    def test_reject_2026_development(self):
        with self.assertRaises(ValueError):
            run_cases(cases(2018),cases(2026),interval="M1",
                      widths=(16,),depths=(1,),seeds=(3,),steps=1)

if __name__=="__main__":
    unittest.main()
