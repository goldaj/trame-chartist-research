"""Synthetic fixtures verify the measurement apparatus; they are never research observations."""
import unittest, io, zipfile, hashlib
import numpy as np
import run_research as r

class ResearchChecks(unittest.TestCase):
    def rows(self,n=180):
        out=[]
        for i in range(n):
            p=100*np.exp(.001*i+.003*np.sin(i))
            out.append((1609459200000+i*r.HOUR,p,p*1.01,p*.99,p*1.002,10+i%13))
        return out

    def test_checksum_and_archive_scope(self):
        name='BTCUSDT-1h-2021-01.zip'; b=io.BytesIO()
        with zipfile.ZipFile(b,'w') as z: z.writestr(name[:-4]+'.csv','a,b')
        body=b.getvalue(); chk=f'{hashlib.sha256(body).hexdigest()}  {name}'.encode()
        self.assertEqual(r.validate_archive(body,chk,name),'a,b')
        with self.assertRaises(AssertionError): r.validate_archive(body+b'x',chk,name)
        with self.assertRaises(AssertionError): r.acquire(('BTCUSDT','2021-11'))

    def test_month_schema_duplicates_and_impossible_bars(self):
        row='1609459200000,100,102,99,101,10,1609462799999,1000,20,5,500,0\n'
        self.assertEqual(r.parse(row,'2021-01')[1]['missing_hours'],743)
        for wrong in [row+row,row.replace(',102,',',98,'),row.replace(',100,',',nan,',1)]:
            with self.assertRaises(AssertionError): r.parse(wrong,'2021-01')
        with self.assertRaises(AssertionError): r.parse(row,'2021-02')

    def test_aggregation_requires_four_parents(self):
        rows=self.rows(12); out=r.aggregate(rows)
        self.assertEqual(len(out),3)
        self.assertEqual(out[0][1],rows[0][1]); self.assertEqual(out[0][4],rows[3][4])
        self.assertEqual(out[0][5],sum(x[5] for x in rows[:4]))
        self.assertEqual(len(r.aggregate(rows[:2]+rows[3:])),2)

    def test_early_close_is_preserved_in_audit_and_excluded(self):
        row='1609459200000,100,102,99,101,10,1609459200999,1000,20,5,500,0\n'
        rows,audit=r.parse(row,'2021-01')
        self.assertEqual(rows,[])
        self.assertEqual(audit['source_observations'],1)
        self.assertEqual(audit['early_close_excluded'][0]['duration_ms'],1000)
        self.assertEqual(audit['missing_hours'],743)
        with self.assertRaises(AssertionError): r.parse(row.replace('1609459200999','1609462800000'),'2021-01')

    def test_strictly_past_reference_and_prefix_invariance(self):
        rows=self.rows(); before=r.features(rows,1)
        changed=list(rows)
        t,o,h,l,c,v=changed[100]; changed[100]=(t,o*3,h*3,l*3,c*3,v*1000)
        after=r.features(changed,1)
        self.assertEqual(before[:35],after[:35])
        self.assertEqual(before[35]['sigma'],after[35]['sigma'])
        self.assertEqual(before[35]['ref'],after[35]['ref'])
        self.assertNotEqual(before[35]['x'],after[35]['x'])
        self.assertEqual(r.features(rows[:100],1),before[:35])

    def test_gap_resets_sixty_five_bar_context(self):
        rows=self.rows(); rows=rows[:80]+rows[81:]
        times=[x['t'] for x in r.features(rows,1)]
        self.assertNotIn(self.rows()[145][0],times)
        self.assertIn(self.rows()[146][0],times)

    def test_continuous_roundtrip_and_fixed_error_bounds(self):
        records=r.features(self.rows(),1); x=np.array([v['x'] for v in records])
        previous=np.array([v['prev'] for v in records]); refs=np.array([v['ref'] for v in records]); true=np.array([v['true'] for v in records])
        prices,volume=r.reconstruct(x,previous,refs)
        np.testing.assert_allclose(prices,true,rtol=1e-14)
        np.testing.assert_allclose(volume,[v['volume'] for v in records],rtol=1e-14)
        decoded,_=r.encode(x,np.ones(len(x)),'fixed',None)
        prices,_=r.reconstruct(decoded,previous,refs)
        error=np.abs(np.log(prices/true))*1e4
        self.assertTrue(np.all(error<=np.array([5,15,15,10])+1e-8))

    def test_quantiles_preserve_zero_and_frozen_codebook(self):
        x=np.array([[-.01,.01,0,.002,.4],[0,.02,.003,0,.5],[.001,0,.004,.005,0]])
        book=r.fit(x); snapshot=repr(book)
        y=np.vstack([x,[1,-1,3,0,4]])
        decoded,ids=r.encode(y,np.ones(len(y)),'quantile64',book)
        self.assertEqual(repr(book),snapshot)
        self.assertTrue(np.all(decoded[y==0]==0))
        self.assertTrue(np.all(ids[y==0]==0))
        self.assertTrue(np.all(decoded[:,2:]>=0))

    def test_event_crossing_is_aggregated_and_censored(self):
        rows=[(0,100,100,100,100,0),(r.HOUR,100,110,100,110,1),(2*r.HOUR,110,110,110,110,0)]
        report=r.event_diagnostic(rows,1)
        self.assertEqual(report['events'],1); self.assertEqual(report['multi_step_events'],1)
        self.assertEqual(report['right_censored_tails'][0]['hours'],1)
        self.assertLess(report['max_abs_residual_log'],.005)

if __name__=='__main__': unittest.main(verbosity=2)
