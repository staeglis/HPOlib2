from hpolib.container.client.abstract_benchmark import AbstractBenchmarkClient


class Branin(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "Branin"
        self._setup()
