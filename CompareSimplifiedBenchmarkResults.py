import os
import argparse
import json
import tabulate
import matplotlib.pyplot as plt
import numpy as np
from utils import generate_target_dir_name, openblas_target_cpu_archs

def tabulate_results(benchmarkparams2archtimes, threshold):
    for benchmark in benchmarkparams2archtimes:
        are_all_below_threshold = True
        for mean, spread, arch in benchmarkparams2archtimes[benchmark]:
            if mean >= threshold:
                are_all_below_threshold = False
                break

        if are_all_below_threshold:
            continue

        print(benchmark)
        means, spreads, archs = [], [], []
        for mean, spread, arch in benchmarkparams2archtimes[benchmark]:
            means.append(mean)
            spreads.append(spread)
            archs.append(arch)
        combined = sorted(zip(means, spreads, archs))
        means = [mean for mean, _, _ in combined]
        spreads = [spread for _, spread, _ in combined]
        archs = [arch for _, _, arch in combined]
        ratios = [mean/means[0] for mean in means]
        print(tabulate.tabulate({"arch": archs, "mean": means, "spread": spreads, "perf_ratios": ratios},
                                headers="keys", tablefmt="pipe"))
        print()

def plot_results(benchmarkparams2archtimes, hardware, threshold):
    for benchmark in benchmarkparams2archtimes:
        are_all_below_threshold = True
        for mean, spread, arch in benchmarkparams2archtimes[benchmark]:
            if mean >= threshold:
                are_all_below_threshold = False
                break

        if are_all_below_threshold:
            continue

        print(benchmark)
        means, spreads, archs = [], [], []
        for mean, spread, arch in benchmarkparams2archtimes[benchmark]:
            means.append(mean)
            spreads.append(spread)
            archs.append(arch)
        combined = sorted(zip(means, spreads, archs))
        means = [mean for mean, _, _ in combined]
        spreads = [spread for _, spread, _ in combined]
        archs = [arch for _, _, arch in combined]
        fig = plt.figure(figsize=(5, 5))
        plt.subplots_adjust(bottom=0.4)
        SMALL_SIZE = 8
        MEDIUM_SIZE = 10
        BIGGER_SIZE = 12

        plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
        plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
        plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
        plt.xticks(rotation=90)
        plt.title("Benchmark: {}\nArchitecture: {}".format(benchmark, hardware), fontweight="bold")
        plt.xlabel("Target OpenBLAS Architecutre", labelpad=10, fontweight='bold')
        plt.ylabel("Time (in s)", fontweight='bold')
        plt.errorbar(archs, means, spreads, linestyle='None', marker='^')
        plt.show()
        fig.savefig("graphs/{}_{}.png".format(benchmark, hardware))
        print()

def process_simplified_benchmark_results(target_archs, hardware, commit_hash, result_dir,
                                         benchmark_name, presentation, threshold):
    arch2benchdata = []
    for target_arch in target_archs:
        simplified_results_dir = os.path.expanduser("{}/simplified_results".format(result_dir))
        os.chdir(simplified_results_dir)
        os.system("mkdir -p graphs")
        filename = "{}/{}.json".format(
            simplified_results_dir,
            generate_target_dir_name(commit_hash, target_arch, benchmark_name)
        )

        if not os.path.exists(filename):
            continue

        with open(filename) as f:
            arch2benchdata.append(json.load(f))

    benchmarks = arch2benchdata[0]["results"].keys()
    benchmarkparams2archtimes = {}
    for benchdata in arch2benchdata:
        benchdata_results = benchdata["results"]
        for benchmark in benchmarks:
            if benchdata_results[benchmark]["params"] is None:
                continue
            if len(benchdata_results[benchmark]["params"]) > 0:
                for i in range(len(benchdata_results[benchmark]["params"])):
                    param = benchdata_results[benchmark]["params"][i]
                    if (benchmark, param) not in benchmarkparams2archtimes:
                        benchmarkparams2archtimes[(benchmark, param)] = []
                    benchmarkparams2archtimes[(benchmark, param)].append((
                        benchdata_results[benchmark]["mean"][i],
                        benchdata_results[benchmark]["spread"][i],
                        benchdata["arch"])
                    )
            else:
                if benchmark not in benchmarkparams2archtimes:
                    benchmarkparams2archtimes[benchmark] = []
                benchmarkparams2archtimes[benchmark].append((
                    benchdata_results[benchmark]["mean"],
                    benchdata_results[benchmark]["spread"],
                    benchdata["arch"])
                )

    print(arch2benchdata[0]["params"])
    if presentation == "table":
        tabulate_results(benchmarkparams2archtimes, threshold)
    elif presentation == "graph":
        plot_results(benchmarkparams2archtimes, hardware, threshold)
    else:
        raise ValueError("{} is not supported.".format(presentation))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse information needed for benchmarking.')
    parser.add_argument('--set-commit-hash', dest='commit_hash', required=True)
    parser.add_argument('--benchmark-name', dest='benchmark_name', default=None)
    parser.add_argument('--hardware', dest='hardware', required=True)
    parser.add_argument('--result-dir', dest='result_dir', required=True)
    parser.add_argument('--presentation', dest='presentation', required=False, default="table")
    parser.add_argument('--threshold', dest='threshold', required=False, default=1e-2)

    args = parser.parse_args()
    process_simplified_benchmark_results(
        openblas_target_cpu_archs[args.hardware], args.hardware,
        args.commit_hash, args.result_dir, args.benchmark_name,
        args.presentation, args.threshold
    )
