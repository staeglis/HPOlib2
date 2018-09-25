if __name__ == "__main__":
    Pyro4.config.REQUIRE_EXPOSE = False

    if len(sys.argv) != 4:
        print("Usage: server.py <importBase> <benchmark>)
        sys.exit()
    importBase = sys.argv[1]
    benchmark = sys.argv[2]

    exec("from hpolib.benchmarks.%s import %s as Benchmark" % (importBase, benchmark))
    b = Benchmark()
