"""S3.0 grammar information-preservation, fabricated numbers ONLY."""
import unittest
from dataclasses import replace

from research.token_grammar.diagnostics import (
    legacy_grammar,continuous_grammar,signed_uniform_grammar,
    fit_signed_quantile_grammar,reconstruction_diagnostics,
)


class GrammarFixtures(unittest.TestCase):
    def test_legacy_really_loses_small_moves_and_direction(self):
        sample=(0.,.1,-.1,4.99,-4.99,5.01,-5.01,9.99,-9.99)
        codec=legacy_grammar()
        tokens=codec.encode(sample)
        self.assertEqual(tokens[0:5],("R0","R0","R0","R0","R0"))
        self.assertEqual(codec.decode(("R0","R1","R-1")),(0.,10.,-10.))
        stats=reconstruction_diagnostics(codec,sample)
        self.assertGreater(stats["direction_lost_count"],0)
        self.assertGreater(stats["absolute_magnitude_reconstruction_mae_bps"],0)
        self.assertFalse(stats["forecast_skill_measured"])

    def test_continuous_is_lossless_and_has_no_discrete_vocabulary(self):
        sample=(0.,.02,-.003,100.51,-205.)
        g=continuous_grammar()
        self.assertEqual(g.decode(g.encode(sample)),sample)
        result=reconstruction_diagnostics(g,sample)
        self.assertEqual(result["direction_lost_count"],0)
        self.assertEqual(result["absolute_magnitude_reconstruction_mae_bps"],0)
        self.assertIsNone(result["empirical_token_entropy_bits"])

    def test_signed_fixed_bins_preserve_nonflat_sign_even_epsilon(self):
        g=signed_uniform_grammar()
        data=(0.,.000001,-.000001,1.,-3.5,6.,-150.,1000.)
        codes=g.encode(data)
        self.assertEqual(codes[0:3],("FLAT","UP0","DOWN0"))
        decoded=g.decode(codes)
        self.assertEqual(decoded[0],0.)
        self.assertTrue(all((a>0)==(b>0) for a,b in
                            zip(data[1:],decoded[1:])))
        self.assertEqual(reconstruction_diagnostics(g,data)
                         ["direction_lost_count"],0)
        with self.assertRaises(ValueError):
            g.decode(("UP-1",))
        with self.assertRaises(ValueError):
            g.decode(("DOWN99",))

    def test_quantile_training_only_is_immutable_to_dev_outliers(self):
        train=(-200.,-100.,-50.,-25.,-10.,-2.,-1.,
               1.,2.,10.,25.,50.,100.,200.)
        g=fit_signed_quantile_grammar(train,bins=4)
        self.assertTrue(g.fit_on_train_only)
        first=g.boundaries_bps
        before=reconstruction_diagnostics(g,(.5,1.1,20.,1000000.))
        after=reconstruction_diagnostics(g,(-999999.,-2.))
        self.assertEqual(g.boundaries_bps,first)
        self.assertGreater(before["above_largest_train_boundary_count"],0)
        self.assertGreater(after["above_largest_train_boundary_count"],0)
        self.assertEqual(reconstruction_diagnostics(g,(-1,1,0))
                         ["direction_lost_count"],0)
        with self.assertRaises(ValueError):
            fit_signed_quantile_grammar([0.]*12,bins=4)

    def test_reject_invalid_nonfinite_or_noncanonical_tokens(self):
        for codec in (legacy_grammar(),signed_uniform_grammar(),
                      continuous_grammar()):
            with self.assertRaises(ValueError):
                codec.encode((1.,float("nan")))
            with self.assertRaises(ValueError):
                codec.encode(())
        with self.assertRaises(ValueError):
            legacy_grammar().decode(("R01",))
        with self.assertRaises(ValueError):
            signed_uniform_grammar().decode(("UP01",))
        with self.assertRaises(ValueError):
            signed_uniform_grammar().decode(("price",))

if __name__=="__main__":
    unittest.main()
