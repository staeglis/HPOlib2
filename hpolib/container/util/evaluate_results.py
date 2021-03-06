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
import sys
import typing

from plottingscripts.utils.merge_test_performance_different_times import fill_trajectory
import plottingscripts.plotting.plot_methods as plot_methods


class DataEvaluation:
    def __init__(self, path):
        self.withContainer = []
        self.withoutContainer = []
        self.rootdir = path
        self.benchmark = "FCNET"

    def parseData(self):
        """ Iterates over the data directories and loads data """

        for d1 in os.listdir(self.rootdir):
            for d2 in os.listdir(self.rootdir + d1):
                for runDir in os.listdir(self.rootdir + d1 + "/" + d2 + "/container/"):
                    filewith = self.rootdir + d1 + "/" + d2 + "/container/" + runDir + "/traj_aclib2.json"
                    self.withContainer.append(self.loadFromFile(filewith))
                for runDir in os.listdir(self.rootdir + d1 + "/" + d2 + "/native/"):
                    filewithout = self.rootdir + d1 + "/" + d2 + "/native/" + runDir + "/traj_aclib2.json"
                    self.withoutContainer.append(self.loadFromFile(filewithout))

    def loadFromFile(self, filepath):
        """ Loads JSON data from a given path """

        result = []
        with open(filepath, encoding='utf-8-sig') as json_file:
            for line in json_file:
                result.append(json.loads(line))
        return result

    def trajectory(self, dataList):
        """ Trajectory """

        perfList = []
        timeList = []

        for l1 in dataList:
            perf = []
            time = []
            for l2 in l1:
                perf.append(l2["cost"])
                time.append(l2["cpu_time"])
            perfList.append(perf)
            timeList.append(time)
        perfList, timeList = fill_trajectory(tuple(perfList), tuple(timeList))
        perfList = numpy.array(perfList).T
        #perfList[perfList > 1] = 1

        return perfList, timeList

    def run(self):
        self.parseData()
        trajContainer = self.trajectory(self.withContainer[0:20])
        trajNative = self.trajectory(self.withoutContainer[0:20])
        fig = plot_methods.plot_optimization_trace_mult_exp(time_list=[trajContainer[1], trajNative[1]],
                                                            performance_list=[trajContainer[0], trajNative[0]],
                                                            title="SMAC on %s" % (self.benchmark),
                                                            name_list=["Container", "Native"],
                                                            #logx=True,
                                                            x_min=50,
                                                            #x_max=250,
                                                            #y_min=0,
                                                            #y_max=2
                                                            )
        matplotlib.pyplot.savefig("plot_%s.png" % (self.benchmark))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: server.py <dataPath>")
        sys.exit()

    path = sys.argv[1]
    de = DataEvaluation(path)
    de.run()
