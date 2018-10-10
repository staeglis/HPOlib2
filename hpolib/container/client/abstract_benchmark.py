'''
@author: Stefan Staeglich
'''

import abc
import json
import numpy
import os
import string
import time
import random

import Pyro4

from ConfigSpace.read_and_write import json as csjson

from hpolib.config import HPOlibConfig


class AbstractBenchmarkClient(metaclass=abc.ABCMeta):
    def _setup(self, gpu=False, imgName=None, **kwargs):
        self.socketId = self.id_generator()
        self.config = HPOlibConfig()

        # Default image name is benchmark name
        if imgName is None:
            imgName = self.bName

        os.system("SINGULARITY_PULLFOLDER=%s singularity pull --name %s.simg %s:%s" % (self.config.image_dir, imgName, self.config.image_source, imgName.lower()))
        iOptions = "%s%s.simg %s" % (self.config.image_dir, imgName, self.socketId)
        sOptions = "instance://%s %s %s&" % (self.socketId, self.bName, self.socketId)
        if gpu:
            iOptions = "--nv " + iOptions
            sOptions = "--nv " + sOptions
        os.system("singularity instance.start %s" % (iOptions))
        os.system("singularity run %s" % (sOptions))

        Pyro4.config.REQUIRE_EXPOSE = False

        u = "PYRO:" + self.socketId + ".unixsock@./u:" + self.config.socket_dir + self.socketId + "_unix.sock"
        self.uri = u.strip()
        self.b = Pyro4.Proxy(self.uri)

        # Handle rng and other optional benchmark arguments
        if 'rng' in kwargs and type(kwargs['rng']) == numpy.random.RandomState:
            (rnd0, rnd1, rnd2, rnd3, rnd4) = kwargs['rng'].get_state()
            rnd1 = [int(number) for number in rnd1]
            kwargs['rng'] = (rnd0, rnd1, rnd2, rnd3, rnd4)
        kwargsStr = json.dumps(kwargs)
        print("Check connection to container and init benchmark")
        while True:
            try:
                self.b.initBenchmark(kwargsStr)
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
