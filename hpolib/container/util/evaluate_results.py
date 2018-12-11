#!/usr/bin/env python3

'''
@author: Stefan Staeglich
'''

import json
import numpy
import os
import sys
import typing

from plottingscripts.utils.merge_test_performance_different_times import fill_trajectory
import plottingscripts.plotting.plot_methods as plot_methods


class DataEvaluation:
    def __init__(self, path):
        self.withContainer = []
        self.withoutContainer = []
        self.rootdir = path

    def parseData(self):
        """ Iterates over the data directories and loads data """

        for d1 in os.listdir(self.rootdir):
            for d2 in os.listdir(self.rootdir + d1):
                filewith = self.rootdir + d1 + "/" + d2 + "/container/run_1/traj_aclib2.json"
                self.withContainer.append(self.loadFromFile(filewith))
                filewithout = self.rootdir + d1 + "/" + d2 + "/native/run_1/traj_aclib2.json"
                self.withoutContainer.append(self.loadFromFile(filewithout))

    def loadFromFile(self, filepath):
        """ Loads JSON data from a given path """

        result = []
        with open(filepath, encoding='utf-8-sig') as json_file:
            for line in json_file:
                result.append(json.loads(line))
        return result

    def trajectory(self, list):
        """ Trajectory """

        perfList = []
        timeList = []

        for l1 in list:
            perf = []
            time = []
            for l2 in l1:
                perf.append(l2["cost"])
                time.append(l2["cpu_time"])
            perfList.append(numpy.array(perf))
            timeList.append(numpy.array(time))
        perfList, timeList = fill_trajectory(perfList, timeList)

        return numpy.array(perfList), numpy.array(timeList)

    def run(self):
        self.parseData()
        trajContainer = self.trajectory(self.withContainer)
        trajNative = self.trajectory(self.withoutContainer)
        print(len(trajContainer[0][0]))
        print(len(trajContainer[1]))
        fig = plot_methods.plot_optimization_trace_mult_exp(time_list=[trajContainer[1], trajNative[1]],
                                                            performance_list=[trajContainer[0], trajNative[0]],
                                                            name_list=["Container", "Native"])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: server.py <dataPath>")
        sys.exit()

    path = sys.argv[1]
    de = DataEvaluation(path)
    de.run()
