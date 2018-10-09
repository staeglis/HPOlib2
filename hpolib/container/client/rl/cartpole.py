from hpolib.container.client.abstract_benchmark import AbstractBenchmarkClient


class CartpoleFull(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "CartpoleFull"
        self._setup(gpu=True, imgName="CartpoleBase")


class CartpoleReduced(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "CartpoleReduced"
        self._setup(gpu=True, imgName="CartpoleBase")
