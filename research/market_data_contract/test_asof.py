"""Adversarial causal-vintage and permission tests, invented prices only."""
import copy
import unittest

from research.market_data_contract.asof import (
    validate_manifest,validate_rows,as_of,forecast_origin_evidence)


MANIFEST={'source_id':'SIM','rights_status':'approved_synthetic','synthetic':True}
def quote(day,price,revision=0,available=None):
    observed=f'2026-01-{day:02d}T00:00:00Z'
    return {'source_id':'SIM','asset':'TOY','observed_at':observed,
            'available_at':available or observed,'price':str(price),
            'unit':'fictional-units/coin','revision':revision}


class PointInTimeContractTests(unittest.TestCase):
    def test_revisions_cannot_be_seen_before_publication(self):
        original=quote(1,'100')
        revised=quote(1,'900',revision=1,available='2026-01-04T00:00:00Z')
        later=quote(2,'102')
        rows=validate_rows([revised,later,original],MANIFEST)
        early=as_of(rows,asset='TOY',knowledge_at='2026-01-02T12:00:00Z')
        self.assertEqual([q.price for q in early],list(map(lambda s:__import__('decimal').Decimal(s),('100','102'))))
        last=as_of(rows,asset='TOY',knowledge_at='2026-01-04T12:00:00Z')
        self.assertEqual(str(last[0].price),'900')
        self.assertEqual(last[0].revision,1)

    def test_late_first_publication_is_not_known_at_event(self):
        late=quote(1,'100',available='2026-01-03T00:00:00Z')
        rows=validate_rows([late,quote(2,'101')],MANIFEST)
        available=as_of(rows,asset='TOY',knowledge_at='2026-01-02T00:00:00Z')
        self.assertEqual([q.observed_at.day for q in available],[2])

    def test_context_and_horizon_purge_split_end(self):
        rows=validate_rows([quote(i,100+i) for i in range(1,10)],MANIFEST)
        valid=forecast_origin_evidence(rows,asset='TOY',knowledge_at='2026-01-05T00:00:00Z',
                              horizon=2,split_end='2026-01-07T00:00:00Z',context=4)
        invalid=forecast_origin_evidence(rows,asset='TOY',knowledge_at='2026-01-05T00:00:00Z',
                              horizon=3,split_end='2026-01-07T00:00:00Z',context=4)
        self.assertTrue(valid['eligible'])
        self.assertFalse(valid['future_price_revealed'])
        self.assertFalse(invalid['eligible'])

    def test_future_revision_does_not_retroactively_mutate_features(self):
        rows=[quote(i,100+i) for i in range(1,6)]
        initial=validate_rows(rows,MANIFEST)
        before=as_of(initial,asset='TOY',knowledge_at='2026-01-05T00:00:00Z')
        rows.append(quote(2,'9999',revision=1,available='2026-01-08T00:00:00Z'))
        altered=validate_rows(rows,MANIFEST)
        after=as_of(altered,asset='TOY',knowledge_at='2026-01-05T00:00:00Z')
        self.assertEqual(before,after)

    def test_real_provider_unlicensed_is_blocked(self):
        bad={'source_id':'ECB_EXR','rights_status':'unverified','synthetic':False}
        with self.assertRaises(PermissionError):
            validate_manifest(bad)
        with self.assertRaises(PermissionError):
            validate_manifest({'source_id':'FAKE_REAL','rights_status':'verified_real','synthetic':False})

    def test_invalid_rows_refused_instead_of_silent_imputation(self):
        standard=quote(1,'100')
        attacks=[
            {'price':'0'}, {'price':'-1'}, {'price':'NaN'}, {'price':'Infinity'},
            {'revision':-1}, {'available_at':'2025-12-31T00:00:00Z'},
            {'observed_at':'2026-01-01T00:00:00'}, {'source_id':'NOT_SIM'},
            {'unit':''}, {'price':100.0}
        ]
        for edit in attacks:
            with self.subTest(edit=edit):
                value=dict(standard,**edit)
                with self.assertRaises((ValueError,TypeError)):
                    validate_rows([value],MANIFEST)

    def test_revisions_must_be_incremental_and_causally_ordered(self):
        for violation in [
            [quote(1,1),quote(1,2,revision=2,available='2026-01-03T00:00:00Z')],
            [quote(1,1),quote(1,2,revision=1,available='2026-01-01T00:00:00Z')],
            [quote(1,1),quote(1,2,revision=0,available='2026-01-03T00:00:00Z')]
        ]:
            with self.assertRaises(ValueError):
                validate_rows(violation,MANIFEST)

    def test_monotone_calendar_without_filling_holidays(self):
        rows=validate_rows([quote(1,100),quote(5,101),quote(9,102)],MANIFEST)
        times=[q.observed_at.day for q in as_of(rows,asset='TOY',knowledge_at='2026-01-10T00:00:00Z')]
        self.assertEqual(times,[1,5,9])


if __name__=='__main__':
    unittest.main()
