from hpolib.container.client.abstract_benchmark import AbstractBenchmarkClient

class Forrester(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "Forrester"
        self.setup()

    def objective_function(self, x, fidelity=1, **kwargs):
        kwargs["fidelity"] = fidelity
        return super().objective_function(x, kwargs)
