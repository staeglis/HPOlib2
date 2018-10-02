import abc
import json
import os
import string
import time
import random

import Pyro4

from ConfigSpace.read_and_write import json as csjson

from hpolib.config import HPOlibConfig


class AbstractBenchmarkClient(metaclass=abc.ABCMeta):
    def _setup(self, gpu=False):
        self.socketId = self.id_generator()
        self.config = HPOlibConfig()

        os.system("singularity pull --name %s.simg %s:%s" % (self.bName, self.config.image_source, self.bName.lower()))
        if gpu:
            os.system("singularity instance.start --nv %s.simg %s" % (self.bName, self.socketId))
        else:
            os.system("singularity instance.start %s.simg %s" % (self.bName, self.socketId))
        os.system("singularity run instance://%s %s&" % (self.socketId, self.socketId))

        Pyro4.config.REQUIRE_EXPOSE = False

        u = "PYRO:" + self.socketId + ".unixsock@./u:" + self.config.socket_dir + self.socketId + "_unix.sock"
        self.uri = u.strip()
        self.b = Pyro4.Proxy(self.uri)
        print("Check connection to container")
        while True:
            try:
                self.b.get_meta_information()
            except Pyro4.errors.CommunicationError:
                print("Still waiting")
                time.sleep(5)
                continue
            break
        print("Connected to container")

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

    def objective_function_test(self, x, **kwargs):
        # Create the arguments as Str
        if (type(x) is list):
            xString = json.dumps(x, indent=None)
            jsonStr = self.b.objective_function_test_list(xString, json.dumps(kwargs))
            return json.loads(jsonStr)
        else:
            # Create the arguments as Str
            cString = json.dumps(x.get_dictionary(), indent=None)
            csString = csjson.write(x.configuration_space, indent=None)
            jsonStr = self.b.objective_function_test(cString, csString, json.dumps(kwargs))
            return json.loads(jsonStr)

    def test(self, *args, **kwargs):
        result = self.b.test(json.dumps(args), json.dumps(kwargs))
        return json.loads(result)

    def get_configuration_space(self):
        jsonStr = self.b.get_configuration_space()
        return csjson.read(jsonStr)

    def get_meta_information(self):
        jsonStr = self.b.get_meta_information()
        return json.loads(jsonStr)

    def __call__ (self, configuration, **kwargs):
        """ Provides interface to use, e.g., SciPy optimizers """
        return(self.objective_function(configuration, **kwargs)['function_value'])

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def __del__(self):
        Pyro4.config.COMMTIMEOUT = 1
        self.b.shutdown()
        os.system("singularity instance.stop %s" % (self.socketId))
        os.remove(self.config.socket_dir + self.socketId + "_unix.sock")
