from hpolib.container.client.abstract_benchmark import AbstractBenchmarkClient

class SvmOnMnist(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "SvmOnMnist"
        self.setup() 


class SvmOnVehicle(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "SvmOnVehicle"
        self.setup() 


class SvmOnCovertype(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "SvmOnCovertype"
        self.setup() 


class SvmOnLetter(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "SvmOnLetter"
        self.setup() 


class SvmOnAdult(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "SvmOnAdult"
        self.setup() 


class SvmOnHiggs(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "SvmOnHiggs"
        self.setup() 
