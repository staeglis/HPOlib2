import numpy as np
import sys
from hpolib.container.client.ml.svm_benchmark import SvmOnVehicle as SvmOnVehicleContainer
from hpolib.benchmarks.ml.svm_benchmark import SvmOnVehicle

try:
    from smac.facade.smac_facade import SMAC
    from smac.scenario.scenario import Scenario
except ImportError:
    print("To run this example you need to install SMAC")
    print("This can be done via `pip install SMAC`")


def main(b, rng):
    # Runs SMAC on a given benchmark
    scenario = Scenario({
        "run_obj": "quality",
        "runcount-limit": b.get_meta_information()['num_function_evals'],
        "cs": b.get_configuration_space(),
        "deterministic": "true",
        "output_dir": "./{:s}/run-{:d}".format(b.get_meta_information()['name'],
                                               10)})

    
    smac = SMAC(scenario=scenario, tae_runner=b,
                rng=myrng)
    x_star = smac.optimize()

    print("Best value found:\n {:s}".format(str(x_star)))
    print("with {:s}".format(str(b.objective_function(x_star))))


if __name__ == "__main__":
    myrng=np.random.RandomState(10)
    print("Running native:")
    main(b=SvmOnVehicle(), rng=myrng)
    print("Running as container:")
    main(b=SvmOnVehicleContainer(), rng=myrng)
