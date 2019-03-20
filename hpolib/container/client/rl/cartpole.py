'''
@author: Stefan Staeglich
'''

from hpolib.container.client.abstract_benchmark import AbstractBenchmarkClient


class CartpoleFull(AbstractBenchmarkClient):
    def __init__(self, gpu=False, **kwargs):
        self.bName = "CartpoleFull"
        img = "CartpoleBase"
        if gpu:
            img = img + "GPU"
        self._setup(imgName=img, gpu=gpu, **kwargs)


class CartpoleReduced(AbstractBenchmarkClient):
    def __init__(self, gpu=False, **kwargs):
        self.bName = "CartpoleReduced"
        img = "CartpoleBase"
        if gpu:
            img = img + "GPU"
        self._setup(imgName=img, gpu=gpu, **kwargs)
