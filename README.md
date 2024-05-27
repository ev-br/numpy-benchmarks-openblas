## About

This repository contains scripts for automatically benchmarking several CPU architectures supported by OpenBLAS simultaneously.

It will also contain scripts for analysing the resulting benchmarking data.

## Steps to use

Inside `numpy` project root execute the following steps,

1. `git clean -fdx`
2. `pip install -e . --no-build-isolation`
3. `python ../numpy-benchmarks-openblas/script.py --set-commit-hash=2da02ea321f557c0cfe0ad6d0e7d8a4354c51103 --benchmark-name=bench_linalg.Eindot.time_matmul_a_b --hardware=x86_64 --result-dir=/path/to/dir/where/results/will/be/stored/by/this/script`

In the third step note the `../numpy-benchmarks-openblas/script.py`. It means that `numpy-benchmarks-openblas` is in the same directory as `numpy`. For example, if `numpy` is present in `~/Quansight/` then `numpy-benchmarks-openblas` should also be present in `~/Quansight/`
