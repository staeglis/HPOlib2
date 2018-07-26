import os
import Pyro4
from hpolib.benchmarks.synthetic_functions import Branin
import random
import string
from ConfigSpace.read_and_write import json as csjson
import json
import ConfigSpace as CS

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class BraninServer():
    def __init__(self):
        if os.path.exists("example_unix.sock"):
            os.remove("example_unix.sock")
        self.daemon = Pyro4.Daemon(unixsocket="example_unix.sock")
        self.b = Branin()
        uri = self.daemon.register(self, "example.unixsock")
        print("Ready. Object uri =", uri)      # print the uri so we can use it in the client later
        self.daemon.requestLoop()              # start the event loop of the server to wait for calls

    def get_configuration_space(self):
        result = self.b.get_configuration_space()
        return csjson.write(result, indent=None)

    def objective_function(self, cString, csString, **kwargs):
        cDict = json.loads(cString)
        cs = csjson.read(csString)
        # configuration = CS.Configuration(cs, cDict, json.loads(kwargs))
        configuration = CS.Configuration(cs, cDict)
        result = self.b.objective_function(configuration)
        return json.dumps(result, indent=None)

    def get_meta_information(self):
        return json.dumps(self.b.get_meta_information(), indent=None)

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    
    @Pyro4.oneway   # in case call returns much later than daemon.shutdown
    def shutdown(self):
        print('shutting down...')
        self.daemon.shutdown()
        os.remove("example_unix.sock")

#Pyro4.config.SERIALIZER='dill'
#Pyro4.config.SERIALIZERS_ACCEPTED = "cloudpickle, dill"

Pyro4.config.REQUIRE_EXPOSE = False
print(Pyro4.config.REQUIRE_EXPOSE)


bp = BraninServer()
