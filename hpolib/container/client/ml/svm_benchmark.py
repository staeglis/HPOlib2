from hpolib.container.client.abstract_benchmark import AbstractBenchmarkClient

class SvmOnVehicle(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "SvmOnVehicle"
        self.setup() 
