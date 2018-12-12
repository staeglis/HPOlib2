'''
@author: Stefan Staeglich
'''

from hpolib.container.client.abstract_benchmark import AbstractBenchmarkClient


class ConvolutionalNeuralNetworkOnMNIST(AbstractBenchmarkClient):
    def __init__(self, **kwargs):
        self.bName = "ConvolutionalNeuralNetworkOnMNIST"
        self._setup(gpu=True, **kwargs)


class ConvolutionalNeuralNetworkOnCIFAR10(AbstractBenchmarkClient):
    def __init__(self, **kwargs):
        self.bName = "ConvolutionalNeuralNetworkOnCIFAR10"
        self._setup(gpu=True, **kwargs)


class ConvolutionalNeuralNetworkOnSVHN(AbstractBenchmarkClient):
    def __init__(self, **kwargs):
        self.bName = "ConvolutionalNeuralNetworkOnSVHN"
        self._setup(gpu=True, **kwargs)
