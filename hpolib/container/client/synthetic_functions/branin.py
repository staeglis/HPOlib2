from hpolib.container.client.abstract_benchmark import AbstractBenchmarkClient


class Branin(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "Branin"
        self._setup(**kwargs)
