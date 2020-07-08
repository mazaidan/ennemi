# MIT License - Copyright Petri Laarne and contributors
# See the LICENSE.md file included in this source code package

"""Benchmarks for ordinary and conditional MI estimation."""

import numpy as np
import timeit

setup = """
from ennemi import estimate_mi
import numpy as np

rng = np.random.default_rng(0)
t = np.arange(N)

a = np.sin(t)
b = np.cos(t) + rng.normal(0, 1, size=N)
c = rng.normal(2, 5, size=N)
d = rng.gamma(1.0, 1.0, size=N)
e = b + 2.0*c
f = c + 2.0*d

data = np.asarray([a, b, c]).T
cond2 = np.asarray([e, f]).T
"""

# Warm up so that possible JIT compilation does not show up in results
print("Warming up...")
warmup_uncond = timeit.repeat("estimate_mi(a, b, k=3)", setup, repeat=1, number=1, globals={"N":50})
warmup_cond = timeit.repeat("estimate_mi(a, b, k=3, cond=c)", setup, repeat=1, number=1, globals={"N":50})
print(f"Warm-up,  MI: {np.min(warmup_uncond):.3} s")
print(f"Warm-up, CMI: {np.min(warmup_cond):.3} s")
print()

mi_bench = "estimate_mi(d, data, lag=[-1, 0, 1, 2], k=3)"
cmi_bench = "estimate_mi(d, data, lag=[-1, 0, 1, 2], k=3, cond=e)"
cmi2_bench = "estimate_mi(d, data, lag=[-1, 0, 1, 2], k=3, cond=cond2)"

for (name, bench) in [ ("MI", mi_bench),
                       ("CMI", cmi_bench),
                       ("CMI2", cmi2_bench) ]:
    for n in [ 100, 400, 1600 ]:
        res = timeit.repeat(bench, setup, repeat=5, number=1, globals={"N": n})
        print(f"{name:<4}, N={n:<4}: min={np.min(res):<6.3} s, mean={np.mean(res):<6.3} s")
