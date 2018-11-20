#!/usr/bin/env python3

'''
@author: Stefan Staeglich
'''

import json
import os
import sys


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
                self.withContainer.append(self.loadFromFile(filewithout))
        print(self.withContainer)


    def loadFromFile(self, filepath):
        """ Loads JSON data from a given path """

        result = []
        with open(filepath, encoding='utf-8-sig') as json_file:
            for line in json_file:
                result.append(json.loads(line))
        return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: server.py <dataPath>")
        sys.exit()

    path = sys.argv[1]
    de = DataEvaluation(path)
    de.parseData()
