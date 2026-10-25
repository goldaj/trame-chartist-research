"""Demonstrate that the bounded FLAT/HIER correction receives gradients.

Artificial bimodal IID codes; NOT market observations, NOT a GPT, and no
scientific comparison of real forecasts. Training budget is illustrative.
"""
import json
import math
import numpy as np

try:
    from .head import A, CORE_N, GRID, Head, hierarchical_logits
except ImportError:
    from head import A, CORE_N, GRID, Head, hierarchical_logits


def synthetic_targets(seed=20261025, n_train=2000, n_test=1000):
    rng = np.random.default_rng(seed)
    codes = np.floor(rng.normal(loc=np.where(rng.integers(2,size=n_train+n_test),8.,-8.),
                                scale=2.0) + 0.5).astype(int)
    return codes[:n_train], codes[n_train:]


def nll(head, targets):
    return float(-np.mean([head.log_prob(int(x)) for x in targets]))


def train_arm(targets, arm, *, iterations=100, learning_rate=1.0):
    if arm not in ('FLAT', 'HIER'):
        raise ValueError('only corrected arms are trainable in this probe')
    counts=np.bincount(targets + 2048,minlength=CORE_N) / len(targets)
    coarse=np.zeros(512)
    bits=np.zeros((3,2))
    flat=np.zeros(CORE_N)
    q_idx=GRID // 8 + 256
    rem=GRID % 8
    for _ in range(iterations):
        raw=flat if arm=='FLAT' else hierarchical_logits(coarse,bits)
        head=Head(mu=0.,sigma=8.,logits=raw,max_sigma=64.)
        prob=np.exp(head.log_core_q + head.correction - head.log_z)
        grad=(prob-counts) * (1.-np.tanh(raw/A)**2)
        if arm=='FLAT':
            flat-=learning_rate*grad
        else:
            coarse-=learning_rate * np.bincount(q_idx,weights=grad,minlength=512)
            for j,shift in enumerate((2,1,0)):
                bits[j]-=learning_rate*np.bincount((rem>>shift)&1,weights=grad,minlength=2)
    raw=flat if arm=='FLAT' else hierarchical_logits(coarse,bits)
    return Head(mu=0.,sigma=8.,logits=raw,max_sigma=64.)


def run():
    train,test=synthetic_targets()
    base=Head(mu=0.,sigma=8.,max_sigma=64.)
    scores={'BASE':{'train_nll':nll(base,train),'test_nll':nll(base,test)}}
    for arm in ('HIER','FLAT'):
        model=train_arm(train,arm)
        scores[arm]={'train_nll':nll(model,train),'test_nll':nll(model,test),
                     'max_abs_correction':float(np.max(np.abs(model.correction)))}
    return {'experiment':'constructed_bimodal_gradient_probe_v0.1',
            'market_data_read':False,'trained_gpt':False,'price_forecasts':False,
            'target_law':'mixture of rounded normal(-8,2), normal(8,2), equal weights',
            'seed':20261025,'train_n':len(train),'test_n':len(test),
            'optimizer':'full_batch_gradient_descent_on_correction_only',
            'fixed_mu':0,'fixed_sigma':8,'iterations':100,'learning_rate':1.,
            'scores':scores,
            'caution':'chosen synthetic example; not a preregistered market test, nor a capacity-fair neural benchmark'}


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
