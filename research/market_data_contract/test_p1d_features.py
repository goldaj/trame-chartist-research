"""Past-only P1-D features; tests use 260 fabricated daily prices."""
from datetime import datetime,timedelta,timezone
import unittest
import numpy as np

from research.market_data_contract.asof import validate_rows,as_of
from research.market_data_contract.p1d_features import p1d_origin_view


MANIFEST={'source_id':'SIM','rights_status':'approved_synthetic','synthetic':True}


def rows_260():
    start=datetime(2026,1,1,tzinfo=timezone.utc)
    out=[]
    for i in range(260):
        stamp=(start+timedelta(days=i)).isoformat().replace('+00:00','Z')
        out.append({'source_id':'SIM','asset':'TOY','observed_at':stamp,
                    'available_at':stamp,'price':str(100+0.08*i+np.sin(i/7.)),
                    'unit':'fictional/TOY','revision':0})
    return out


class CodecTests(unittest.TestCase):
    def test_256_values_only_past_and_64_increments(self):
        rows=validate_rows(rows_260(),MANIFEST)
        cutoff='2026-09-18T00:00:00Z'
        snapshot=p1d_origin_view(rows,asset='TOY',knowledge_at=cutoff)
        self.assertEqual(snapshot['n'],256)
        self.assertEqual(len(snapshot['q_codes']),256)
        self.assertEqual(snapshot['q_codes'][-1],0)
        self.assertFalse(snapshot['future_values_used'])
        self.assertGreater(snapshot['scale'],0)
        self.assertTrue(all(isinstance(k,int) for k in snapshot['q_codes']))

    def test_unavailable_revision_and_future_values_not_in_features(self):
        raw=rows_260()
        known=validate_rows(raw,MANIFEST)
        decision='2026-09-18T00:00:00Z'
        before=p1d_origin_view(known,asset='TOY',knowledge_at=decision)
        # Revision of an OLD event published after decision.
        revised=dict(raw[15],revision=1,price='999999',
                     available_at='2026-09-23T00:00:00Z')
        raw.append(revised)
        changed=validate_rows(raw,MANIFEST)
        after=p1d_origin_view(changed,asset='TOY',knowledge_at=decision)
        self.assertEqual(before,after)

    def test_refuse_context_not_fixed_or_not_available(self):
        rows=validate_rows(rows_260()[:200],MANIFEST)
        with self.assertRaises(ValueError):
            p1d_origin_view(rows,asset='TOY',knowledge_at='2026-09-18T00:00:00Z')
        with self.assertRaises(ValueError):
            p1d_origin_view(rows,asset='TOY',knowledge_at='2026-09-18T00:00:00Z',context=100)


if __name__=='__main__':
    unittest.main()
