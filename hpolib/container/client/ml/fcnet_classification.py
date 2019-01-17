'''
@author: Stefan Staeglich
'''

from hpolib.container.client.abstract_benchmark import AbstractBenchmarkClient


class ClassificationNeuralNetwork(AbstractBenchmarkClient):
    def __init__(self, **kwargs):
        self.bName = "ClassificationNeuralNetwork"
        self._setup(**kwargs)
