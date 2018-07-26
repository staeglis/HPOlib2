This folder contains a prototype for running HPOlib2 benchmarks as containers.
At the moment it uses Singularity. So you have to install Singularity first:
https://singularity.lbl.gov/install-linux

The mechanism used is known as RPC and is implemented by Pyro4. For running the
benchmark inside the container there exist a client class simulating the
original API.

The client class controls the container. The RPC server is implemented by
a server class. The server class orientates on the original API and runs inside
the container. Both classes are using JSON and Pyro4 to communicate.

There is also an modified example. To run it you need an actual git snapshot of
ConfigSpace.
