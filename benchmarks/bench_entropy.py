# MIT License - Copyright Petri Laarne and contributors
# See the LICENSE.md file included in this source code package

"""Benchmarks for entropy estimation."""

import numpy as np
import timeit

setup = """
from ennemi import estimate_entropy
import numpy as np

rng = np.random.default_rng(0)
cov = np.array([
    [ 1.0,  0.5,  0.6, -0.2],
    [ 0.5,  1.0,  0.7, -0.5],
    [ 0.6,  0.7,  2.0, -0.1],
    [-0.2, -0.5, -0.1,  0.5]])
data = rng.multivariate_normal([0, 0, 0, 0], cov, size=4000)
"""

bench_1d = "estimate_entropy(data[:N,0], k=3)"
bench_4d = "estimate_entropy(data[:N,:], k=3, multidim=True)"
bench_independent = "estimate_entropy(data[:N,:], k=3)"
bench_cond = "estimate_entropy(data[:N,:3], k=3, cond=data[:N,3])"

# Warm up so that possible JIT compilation does not show up in results
print("Warming up...")
warmup_1d = timeit.repeat(bench_1d, setup, repeat=1, number=1, globals={"N": 20})
print(f"Warm-up, 1D: {np.min(warmup_1d):.3} s")
warmup_4d = timeit.repeat(bench_4d, setup, repeat=1, number=1, globals={"N": 20})
print(f"Warm-up, 4D: {np.min(warmup_1d):.3} s")
print()

for (name, bench) in [ ("1D", bench_1d),
                       ("4x1D", bench_independent),
                       ("4D", bench_4d),
                       ("Cond 3x1D", bench_cond) ]:
    for n in [ 250, 1000, 4000 ]:
        res = timeit.repeat(bench, setup, repeat=5, number=1, globals={"N": n})
        print(f"{name:>9}, N={n:<4}: min={np.min(res):<6.3} s, mean={np.mean(res):<6.3} s")