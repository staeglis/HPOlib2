import Pyro4
# from hpolib.abstract_benchmark import AbstractBenchmark

import json
import os
import string
import time
import random

import ConfigSpace as CS

from ConfigSpace.read_and_write import json as csjson

class Branin():
    def __init__(self):
        #subprocess.call(['python3', 'server.py', '&'])
        self.socketId = self.id_generator()

        os.system("singularity pull --name Branin.simg shub://staeglis/HPOlib2:branin")
        os.system("singularity run Branin.simg %s&" % self.socketId)
        time.sleep(10)
        
        Pyro4.config.REQUIRE_EXPOSE = False
        
        u = "PYRO:" + self.socketId + ".unixsock@./u:" + self.socketId + "_unix.sock"
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
        return json.loads(dictionary)
    
    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
         return ''.join(random.choice(chars) for _ in range(size))
    
    def __del__(self):
        self.b.shutdown()
        os.remove(self.socketId + "_unix.sock")
