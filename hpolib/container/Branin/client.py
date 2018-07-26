import Pyro4
import ConfigSpace

# from hpolib.abstract_benchmark import AbstractBenchmark

import json
import re
import os
#import subprocess
import time

import ConfigSpace as CS

from ConfigSpace.read_and_write import json as csjson

class Branin():
    def __init__(self):
        #subprocess.call(['python3', 'server.py', '&'])
        if not os.path.exists("Branin.img"):
            os.system("singularity pull --name Branin.img shub://staeglis/HPOlib2:branin")
        os.system("singularity run Branin.img &")
        time.sleep(10)
        
        #Pyro4.config.SERIALIZER="cloudpickle"
        #Pyro4.config.SERIALIZERS_ACCEPTED = "pickle, dill"
        Pyro4.config.REQUIRE_EXPOSE = False
        u = "PYRO:example.unixsock@./u:example_unix.sock"
        self.uri = u.strip()
        self.b = Pyro4.Proxy(self.uri)

    def objective_function(self, x, **kwargs):
        # Create the arguments as Str
        cString = json.dumps(x.get_dictionary(), indent=None)
        csString = csjson.write(x.configuration_space, indent=None)
        # arguments += ", '" + json.dumps(kwargs) + "'"
        jsonStr = self.b.objective_function(cString, csString)
        return json.loads(jsonStr)

    def get_configuration_space(self):
        jsonStr = self.b.get_configuration_space()
        return csjson.read(jsonStr)
    
    def get_meta_information(self):
        dictionary = self.b.get_meta_information()
        return json.loads(eval(dictionary['text/plain']))
    
    def __del__(self):
        self.b.shutdown()
