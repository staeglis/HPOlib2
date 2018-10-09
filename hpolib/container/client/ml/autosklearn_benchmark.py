from hpolib.container.client.abstract_benchmark import AbstractBenchmarkClient


class Sick(AbstractBenchmarkClient):
    def __init__(self, **kwargs):
        self.bName = "Sick"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class Splice(AbstractBenchmarkClient):
    def __init__(self, **kwargs):
        self.bName = "Splice"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class Adult(AbstractBenchmarkClient):
    def __init__(self, **kwargs):
        self.bName = "Adult"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class KROPT(AbstractBenchmarkClient):
    def __init__(self, **kwargs):
        self.bName = "KROPT"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class MNIST(AbstractBenchmarkClient):
    def __init__(self, **kwargs):
        self.bName = "MNIST"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class Quake(AbstractBenchmarkClient):
    def __init__(self, **kwargs):
        self.bName = "Quake"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class PC4(AbstractBenchmarkClient):
    def __init__(self, **kwargs):
        self.bName = "PC4"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class KDDCup09_appetency(AbstractBenchmarkClient):
    def __init__(self, **kwargs):
        self.bName = "KDDCup09_appetency"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class MagicTelescope(AbstractBenchmarkClient):
    def __init__(self, **kwargs):
        self.bName = "MagicTelescope"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class OVABreast(AbstractBenchmarkClient):
    def __init__(self, **kwargs):
        self.bName = "OVABreast"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class Covertype(AbstractBenchmarkClient:
    def __init__(self, **kwargs):
        self.bName = "Covertype"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)


class FBIS_WC(AbstractBenchmarkClient):
    def __init__(self, **kwargs):
        self.bName = "FBIS_WC"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark", **kwargs)
