from hpolib.container.client.abstract_benchmark import AbstractBenchmarkClient


class AutoSklearnBenchmark(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "AutoSklearnBenchmark"


class MulticlassClassificationBenchmark(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "MulticlassClassificationBenchmark"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark")


class Sick(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "Sick"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark")


class Splice(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "Splice"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark")


class Adult(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "Adult"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark")


class KROPT(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "KROPT"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark")


class MNIST(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "MNIST"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark")


class Quake(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "Quake"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark")


class PC4(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "PC4"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark")


class KDDCup09_appetency(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "KDDCup09_appetency"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark")


class MagicTelescope(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "MagicTelescope"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark")


class OVABreast(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "OVABreast"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark")


class Covertype(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "Covertype"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark")


class FBIS_WC(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "FBIS_WC"
        self._setup(gpu=True, imgName="AutoSklearnBenchmark")
