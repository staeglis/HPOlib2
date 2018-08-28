import os
import Pyro4
from hpolib.benchmarks.synthetic_functions import Forrester
import random
import string
import sys
from ConfigSpace.read_and_write import json as csjson
import json
import ConfigSpace as CS

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class ForresterServer():
    def __init__(self, socketId):
        self.pyroRunning = True

        self.socketId = socketId
        socketPath = self.socketId + "_unix.sock"
        if os.path.exists(socketPath):
            os.remove(socketPath)
        self.daemon = Pyro4.Daemon(unixsocket=socketPath)
        self.b = Branin()
        uri = self.daemon.register(self, self.socketId + ".unixsock")
        print("Ready. Object uri =", uri)      # print the uri so we can use it in the client later
        self.daemon.requestLoop(loopCondition=lambda: self.pyroRunning)              # start the event loop of the server to wait for calls

    def get_configuration_space(self):
        result = self.b.get_configuration_space()
        return csjson.write(result, indent=None)

    def objective_function(self, xString, fidelity, kwargs):
        x = json.loads(xString)
        if kwargs == "{}":
            result = self.b.objective_function(x)
        else:
            result = self.b.objective_function(x, json.loads(kwargs))
        return json.dumps(result, indent=None)

    def get_meta_information(self):
        return json.dumps(self.b.get_meta_information(), indent=None)

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    
    @Pyro4.oneway   # in case call returns much later than daemon.shutdown
    def shutdown(self):
        print('shutting down...')
        self.pyroRunning = False
        self.daemon.shutdown()

if __name__ == "__main__":
    Pyro4.config.REQUIRE_EXPOSE = False
    print(Pyro4.config.REQUIRE_EXPOSE)
    Pyro4.config.COMMTIMEOUT=0.5

    if len(sys.argv) != 2:
        print("Usage: server.py <socketId>")
        sys.exit()
    socketId = sys.argv[1]

    bp = BraninServer(socketId)
