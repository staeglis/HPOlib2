import Pyro4

import json
import os
import string
import time
import random

import ConfigSpace as CS

from ConfigSpace.read_and_write import json as csjson

class AbstractBenchmarkClient():
    def setup(self):
        self.socketId = self.id_generator()

        os.system("singularity pull --name %s.simg shub://staeglis/HPOlib2:%s" % (self.bName, self.bName.lower()))
        os.system("singularity run %s.simg %s&" % (self.bName, self.socketId))
        time.sleep(10)
        
        Pyro4.config.REQUIRE_EXPOSE = False
        Pyro4.config.COMMTIMEOUT=1
        
        u = "PYRO:" + self.socketId + ".unixsock@./u:" + self.socketId + "_unix.sock"
        self.uri = u.strip()
        self.b = Pyro4.Proxy(self.uri)
        
    def objective_function(self, x, **kwargs):
        # Create the arguments as Str
        if (type(x) is list):
            xString = json.dumps(x, indent=None)
            jsonStr = self.b.objective_function_list(xString, json.dumps(kwargs))
            return json.loads(jsonStr)
        else:
            # Create the arguments as Str
            cString = json.dumps(x.get_dictionary(), indent=None)
            csString = csjson.write(x.configuration_space, indent=None)
            jsonStr = self.b.objective_function(cString, csString, json.dumps(kwargs))
            return json.loads(jsonStr)

    def get_configuration_space(self):
        jsonStr = self.b.get_configuration_space()
        return csjson.read(jsonStr)
    
    def get_meta_information(self):
        jsonStr = self.b.get_meta_information()
        return json.loads(jsonStr)
    
    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
         return ''.join(random.choice(chars) for _ in range(size))
    
    def __del__(self):
        self.b.shutdown()
        os.remove(self.socketId + "_unix.sock")
 
