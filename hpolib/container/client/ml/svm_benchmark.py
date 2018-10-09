from hpolib.container.client.abstract_benchmark import AbstractBenchmarkClient


class SvmOnMnist(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "SvmOnMnist"
        self.setup(**kwargs)


class SvmOnVehicle(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "SvmOnVehicle"
        self._setup(**kwargs)


class SvmOnCovertype(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "SvmOnCovertype"
        self._setup(**kwargs)


class SvmOnLetter(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "SvmOnLetter"
        self._setup(**kwargs)


class SvmOnAdult(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "SvmOnAdult"
        self._setup(**kwargs)


class SvmOnHiggs(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "SvmOnHiggs"
        self._setup(**kwargs)
