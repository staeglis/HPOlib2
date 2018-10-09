from hpolib.container.client.abstract_benchmark import AbstractBenchmarkClient


class CartpoleFull(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "CartpoleFull"
        self._setup(gpu=True, imgName="CartpoleBase", **kwargs)


class CartpoleReduced(AbstractBenchmarkClient, **kwargs):
    def __init__(self):
        self.bName = "CartpoleReduced"
        self._setup(gpu=True, imgName="CartpoleBase", **kwargs)
