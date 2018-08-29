import Pyro4
# from hpolib.container.abstract_benchmark.client import AbstractClient

import json
import os
import string
import time
import random

import ConfigSpace as CS

from ConfigSpace.read_and_write import json as csjson

from hpolib.container.client.abstract_benchmark import AbstractBenchmarkClient

class Branin(AbstractBenchmarkClient):
    def __init__(self):
        self.bName = "Branin"
        self.setup()
