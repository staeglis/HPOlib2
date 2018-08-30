import os
import Pyro4
import random
import string
import sys
from ConfigSpace.read_and_write import json as csjson
import json
import ConfigSpace as CS

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class BenchmarkServer():
    def __init__(self, benchmark, socketId):
        self.pyroRunning = True

        self.socketId = socketId
        socketPath = self.socketId + "_unix.sock"
        if os.path.exists(socketPath):
            os.remove(socketPath)
        self.daemon = Pyro4.Daemon(unixsocket=socketPath)

        self.b = Benchmark()
        uri = self.daemon.register(self, self.socketId + ".unixsock")
        print("Ready. Object uri =", uri)      # print the uri so we can use it in the client later
        self.daemon.requestLoop(loopCondition=lambda: self.pyroRunning)              # start the event loop of the server to wait for calls

    def get_configuration_space(self):
        result = self.b.get_configuration_space()
        return csjson.write(result, indent=None)

    def objective_function_list(self, xString, fidelity, kwargs="{}"):
        x = json.loads(xString)
        if kwargs == "{}":
            result = self.b.objective_function(x)
        else:
            result = self.b.objective_function(x, json.loads(kwargs))
        return json.dumps(result, indent=None)
    
    def objective_function(self, cString, csString, kwargs):
        cDict = json.loads(cString)
        cs = csjson.read(csString)
        configuration = CS.Configuration(cs, cDict)
        if kwargs == "{}":
            result = self.b.objective_function(configuration)
        else:
            result = self.b.objective_function(configuration, json.loads(kwargs))
        return json.dumps(result, indent=None)

    def get_meta_information(self):
        return json.dumps(self.b.get_meta_information(), indent=None)

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    
    @Pyro4.oneway   # in case call returns much later than daemon.shutdown
    def shutdown(self):
        print('shutting down...')
        Pyro4.config.COMMTIMEOUT = 0.5
        self.pyroRunning = False
        self.daemon.shutdown()

if __name__ == "__main__":
    Pyro4.config.REQUIRE_EXPOSE = False

    if len(sys.argv) != 4:
        print("Usage: server.py <importBase> <benchmark> <socketId>")
        sys.exit()
    importBase = sys.argv[1]
    benchmark = sys.argv[2]
    socketId = sys.argv[3]

    exec("from hpolib.benchmarks.%s import %s as Benchmark" % (importBase, benchmark))
    bp = BenchmarkServer(benchmark, socketId)
