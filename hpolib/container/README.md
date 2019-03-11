# What's this?
This folder contains code for running HPOlib2 benchmarks as containers.

The mechanism used is known as RPC and is implemented by Pyro4. For running the
benchmark inside the container there exist a client class simulating the
original API.

The client class controls the container. The RPC server is implemented by
a server class. The server class orientates on the original API and runs inside
the container. Both classes are using JSON and Pyro4 to communicate.

# How can I use it?
There are some modified examples. To run it you need at least ConfigSpace 0.4.7.
Also you need Pyro4. On Ubuntu you can install it with
* sudo apt install pyro4 python3-pyro4 -y

You can run the example with
* python3 example.py

At the moment it uses Singularity. So you have to install Singularity first:
https://singularity.lbl.gov/install-linux

# How can I build my own container?
For providing a new benchmark as container, you have to write a client class and
a Singularity recipe.

## The client class
The client class should have the same name as the original benchmark class.
It should be stored inside the client subfolder. The client subfolder has the same
hirachy as the folder 'benchmarks'.

For the client class you have to write at least a constructor. Inside the constructor
you have to set the property `self.bName`. Also you have to call the
`self.setup(**kwargs)`method. Such a minimal example you can find in
'client/ml/svm_benchmark.py'.

If you want to use a container for more than one benchmark, you maybe have to set the
named argument imgName of the method `self._setup()`. Such an example you can find
in 'client/synthetic_functions/levy.py'.

If your benchmark needs GPU support, you have to set the named argument gpu of the
method `self._setup()` to `True`. Look in 'client/ml/convnet_net.py' for getting an
example.

If your benchmark constructor has some mandatory arguments, this should also be true
for your client class. You have to add the values to the kwargs dictionary. Look in
'client/ml/fcnet_classification.py' for getting an example.

You have to check your return data types. If they aren't serializable with Pyro4,
you think about using other data types. If this isn't possible, you have to adjust
the encoder class BenchmarkEncoder defined in 'server/abstract_benchmark.py'. The
deserialization should be done inside your client class. For this you have to write
some additional methods. Look in 'client/ml/autosklearn_benchmark.py' for getting
an example.

If you provide some variants of your benchmark via sub classes and your client
classes are getting more complicated, you should write an client base class.
