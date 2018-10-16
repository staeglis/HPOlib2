import time
import numpy as np

try:
    from hpolib.benchmarks.ml.autosklearn_benchmark import Covertype
except ModuleNotFoundError:
    from hpolib.container.client.ml.autosklearn_benchmark import Covertype

import ConfigSpace


# Perform random search on the Branin function

b = Covertype()
start = time.time()

values = []

cs = b.get_configuration_space()

for i in range(2):
    configuration = cs.sample_configuration()
    # s = time.time()
    rval = b.objective_function(configuration, fold=10, folds=10)
    # print("Done, took %.2f s" % ((time.time() - s)))
    loss = rval['function_value']
    values.append(loss)

print(np.min(values))

print("Done, took totally %.2f s" % ((time.time() - start)))

