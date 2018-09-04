import numpy as np

import hpolib.benchmarks.synthetic_functions as hpobench
from client import BenchmarkClient as Forrester
import client
client.benchmark = "Forrester"

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# Use the 1d Forrester function and add artifical noise depending
# on the 'dateset size'
f = hpobench.SyntheticNoiseAndCost(Forrester(), 0, 2, 0.1, 1, 2, 2)

# grid for plotting
X = np.linspace(0, 1, 50)
d = np.linspace(0, 1, 50)
X, D = np.meshgrid(X, d)

# compute target values and costs
T = []
C = []

for x, d in zip(X.flatten(), D.flatten()):
    mew = f.objective_function([x], dataset_fraction=d)
    T.append(mew['function_value'])
    C.append(mew['cost'])
T = np.array(T).reshape(X.shape)
C = np.array(C).reshape(X.shape)

# make some decent looking plots
fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')
ax.set_title('The function in the \'extended space\'')
ax.set_xlabel('x')
ax.set_ylabel('dataset fraction')
ax.set_zlabel('f(x,dataset_fraction')
surf = ax.plot_surface(X, D, T, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

ax = fig.add_subplot(122, projection='3d')
ax.set_title('The associated cost')
ax.set_xlabel('x')
ax.set_ylabel('dataset fraction')
ax.set_zlabel('cost')
surf = ax.plot_surface(X, D, C, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

plt.show()
