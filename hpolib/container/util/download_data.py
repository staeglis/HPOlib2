import sys
import time

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: server.py <importBase> <benchmark>")
        sys.exit()
    importBase = sys.argv[1]
    benchmark = sys.argv[2]

    exec("from hpolib.benchmarks.%s import %s as Benchmark" % (importBase, benchmark))
    start = time.time()
    b = Benchmark()
    print("Data download done, took totally %.2f s" % ((time.time() - start)))
