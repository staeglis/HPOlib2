from hpbandster.core.worker import Worker
from hpolib.benchmarks.rl.cartpole import CartpoleReduced as Benchmark
from hpolib.container.client.rl.cartpole import CartpoleReduced as BenchmarkContainer

import argparse
import pickle
import time

import hpbandster.core.nameserver as hpns
import hpbandster.core.result as hpres

from hpbandster.optimizers import BOHB as BOHB


class HpolibWorker(Worker):
    def __index__(self, b, *args, sleep_interval=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.sleep_interval = sleep_interval
        self.b = b

    def compute(self, config, budget, working_directory, *args, **kwargs):
        return self.b.objective_function(config, budget=budget)

    def get_configspace(self):
        return self.b.get_configuration_space()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run BOHB on a HPOLib2 benchmark')
    parser.add_argument('--min_budget',   type=float, help='Minimum budget used during the optimization.',    default=9)
    parser.add_argument('--max_budget',   type=float, help='Maximum budget used during the optimization.',    default=243)
    parser.add_argument('--n_iterations', type=int,   help='Number of iterations performed by the optimizer', default=4)
    parser.add_argument('--n_workers', type=int,   help='Number of workers to run in parallel.', default=2)
    parser.add_argument('--worker', help='Flag to turn this into a worker process', action='store_true')
    parser.add_argument('--run_id', type=str, help='A unique run id for this optimization run. An easy option is to use the job id of the clusters scheduler.')
    parser.add_argument('--nic_name',type=str, help='Which network interface to use for communication.')
    parser.add_argument('--shared_directory',type=str, help='A directory that is accessible for all processes, e.g. a NFS share.')
    parser.add_argument('--benchmark_type', type=str,   help='Benchmark type', default="container")

    args = parser.parse_args()

    # Every process has to lookup the hostname
    host = hpns.nic_name_to_host(args.nic_name)

    # Start a nameserver:
    # We now start the nameserver with the host name from above and a random open port (by setting the port to 0)
    NS = hpns.NameServer(run_id=args.run_id, host=host, port=0, working_directory=args.shared_directory)
    ns_host, ns_port = NS.start()

    # Most optimizers are so computationally inexpensive that we can affort to run a
    # worker in parallel to it. Note that this one has to run in the background to
    # not plock!
    if args.benchmark_type == "container":
        b = BenchmarkContainer()
    else:
        b = Benchmark()
    w = HpolibWorker(b, sleep_interval=0.5, run_id=args.run_id, host=host, nameserver=ns_host, nameserver_port=ns_port)
    w.run(background=True)
    # Run an optimizer
    # We now have to specify the host, and the nameserver information
    bohb = BOHB(configspace=HpolibWorker.get_configspace(),
                run_id=args.run_id,
                host=host,
                nameserver=ns_host,
                nameserver_port=ns_port,
                min_budget=args.min_budget, max_budget=args.max_budget)

    # In a cluster environment, you usually want to store the results for later analysis.
    # One option is to simply pickle the Result object
    with open(os.path.join(args.shared_directory, args.benchmark_type + '-results.pkl'), 'wb') as fh:
        pickle.dump(res, fh)

    # Step 4: Shutdown
    # After the optimizer run, we must shutdown the master and the nameserver.
    bohb.shutdown(shutdown_workers=True)
    NS.shutdown()
