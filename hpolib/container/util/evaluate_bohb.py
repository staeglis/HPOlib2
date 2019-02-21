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
            timeDict = {}
            perfDict = {}
            for t, p, b in zip(l1["times_finished"], l1["losses"], l1["budgets"]):
                if b not in timeDict:
                    timeDict[b] = [0, t]
                    perfDict[b] = [100000, p]
                else:
                    timeDict[b].append(t)
                    perfDict[b].append(p)
            for b in l1["budgets"]:
                perfDict[b][0] = perfDict[b][1]
                perfList.append(perfDict[b])
                timeList.append(timeDict[b])
        perfList, timeList = fill_trajectory(tuple(perfList), tuple(timeList))
        perfList = numpy.array(perfList).T
        print(timeList)
        print(perfList[0])

        return [p[1:-1] for p in perfList], timeList[1:-1]

    def run(self):
        self.parseData()
        print(self.withContainer[1])
        trajContainer = self.trajectory(self.withContainer)
        trajNative = self.trajectory(self.withoutContainer)
        fig = plot_methods.plot_optimization_trace_mult_exp(time_list=[trajContainer[1], trajNative[1]],
                                                            performance_list=[trajContainer[0], trajNative[0]],
                                                            name_list=["Container", "Native"],
                                                            ylabel="loss",
                                                            agglomeration="median",
                                                            #logx=True,
                                                            #x_min=1,
                                                            #x_max=30000,
                                                            y_max=3000
                                                            )
        matplotlib.pyplot.savefig("bohb_plot.png")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: evaluate_bohb.py <dataPath>")
        sys.exit()

    path = sys.argv[1]
    de = BohbEvaluation(path)
    de.run()