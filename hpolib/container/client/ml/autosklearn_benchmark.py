from hpolib.container.client.abstract_benchmark import AbstractBenchmarkClient


class Sick(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "Sick"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class Splice(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "Splice"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class Adult(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "Adult"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class KROPT(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "KROPT"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class MNIST(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "MNIST"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class Quake(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "Quake"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class PC4(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "PC4"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class KDDCup09_appetency(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "KDDCup09_appetency"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class MagicTelescope(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "MagicTelescope"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class OVABreast(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "OVABreast"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class Covertype(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "Covertype"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class FBIS_WC(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "FBIS_WC"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)
