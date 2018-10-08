from hpolib.container.client.abstract_benchmark import AbstractBenchmarkClient

class CartpoleBase(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "CartpoleBase"
        self._setup()


class CartpoleFull(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "CartpoleFull"
        self._setup()


class CartpoleReduced(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "CartpoleReduced"
        self._setup()
