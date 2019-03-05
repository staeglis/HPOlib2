#!/usr/bin/env python3

'''
@author: Stefan Staeglich
'''

from collections import OrderedDict
import json
import matplotlib.pyplot
import numpy
import os
import pandas
import pickle
import sys
import typing

import hpbandster.core.result as hpres
import hpbandster.visualization as hpvis

from plottingscripts.utils.merge_test_performance_different_times import fill_trajectory
import plottingscripts.plotting.plot_methods as plot_methods


class BohbEvaluation:
    def __init__(self, path):
        self.withContainer = []
        self.withoutContainer = []
        self.rootdir = path
        self.benchmark = "Cartpole"

    def parseData(self):
        """ Iterates over the data directories and loads data """

        for d in os.listdir(self.rootdir):
            filewith = self.rootdir + d + "/container-results.pkl"
            self.withContainer.append(self.loadFromFile(filewith))
            filewithout = self.rootdir + d + "/native-results.pkl"
            self.withoutContainer.append(self.loadFromFile(filewithout))

    def loadFromFile(self, filepath):
        """ Loads JSON data from a given path """

        result = []
        with open(filepath, "rb") as json_file:
            result = pickle.load(json_file)
            return result.get_incumbent_trajectory()

    def trajectory(self, dataList):
        """ Trajectory """

        perfList = []
        timeList = []

        for l1 in dataList:
            time = l1["times_finished"]
            perf = l1["losses"]
            t0 = time[0]
            for i in range(0, len(time) - 1):
                time[i] = time[i] - t0
            perfList.append(perf)
            timeList.append(time)
        perfList, timeList = fill_trajectory(tuple(perfList), tuple(timeList))
        perfList = numpy.array(perfList).T

        return [p[1:-1] for p in perfList], timeList[1:-1]

    def run(self):
        self.parseData()
        trajContainer = self.trajectory(self.withContainer)
        trajNative = self.trajectory(self.withoutContainer)
        fig = plot_methods.plot_optimization_trace_mult_exp(time_list=[trajContainer[1], trajNative[1]],
                                                            performance_list=[trajContainer[0], trajNative[0]],
                                                            title="BOHB on %s" % (self.benchmark),
                                                            name_list=["Container", "Native"],
                                                            ylabel="loss",
                                                            agglomeration="mean",
                                                            #logx=True,
                                                            #x_min=1,
                                                            #x_max=30000,
                                                            y_max=3000
                                                            )
        matplotlib.pyplot.savefig("bohb_plot_%s.png" % (self.benchmark))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: evaluate_bohb.py <dataPath>")
        sys.exit()

    path = sys.argv[1]
    de = BohbEvaluation(path)
    de.run()
