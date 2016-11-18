import sys
import os
import os.path
import gzip
import getopt
import copy
import numpy as np

#tracerParts:
#fitler,adapter,select,trace,shuffle,send,gather,frame
#method.totaltime=fitler+adapter,select,trace,shuffle,send,gather
#count number of trials by counting number of "generate cammera rays"
##1 dict with 1 scheduler, keys are tracerParts, values are arrays


class ParseData:
    def __init__(self):
        self.numThreads = -1
        self.adapter = None
        self.scheduler = None
        self.numTrials = -1
        self.data = None
        self.dataSet = False

    def setNumThreads(self,numThreads):
        self.numThreads = numThreads

    def setAdapter(self,adapter):
        self.adapter = adapter

    def setData(self):
        self.data = {} #incomplete
        self.dataSet = True

    def getData(self,):
        assert (self.dataSet), "Error: Data not set"
        return self.data

    def getDataEntry(self,tracerPartKey):
        print "not done yet"

    def getNumThreads(self,):
        return self.numThreads

    def getAdapter(self,):
        return self.adapter

    def getScheduler(self,):
        return self.scheduler

    def numTrials(self,):
        return self.numTrials

class gravitTimeParser:
  def __init__(self):
    pass
    self.filename = ""
    self.fileSet = False
    self.data = ParseData()

  def parseFile(self,filename):
    self.filename = filename
    self.fileSet = True
    self.parse()

  def printRunInfo(self,):
    assert (self.fileSet), "Error: filename not set"
    print "The run for file", self.filename, "used", self.data.getNumThreads(), "threads"
    #print "  and took", #gravitTimeParser.getDataEntry("Total","wallmax"), "seconds"

  def parse(self,):
    assert (self.fileSet), "Error: filename not set"

    # Parse the file
    extension = os.path.splitext(self.filename)[1]
    if (extension == '.gz') :
      #lines=gzip.open(self.filename,'r')
      self.fid = gzip.open(self.filename,'r')
    else:
      self.fid = open(self.filename,'r')

    for line in self.fid.readlines():
        #get number of threads
        if ("Initialized") and ("threads") in line:
          print line
          numThreads = line.split()[3]
          self.data.setNumThreads(numThreads)
        #get adapter
        if ("Using") and ("adapter") in line:
            adapter = line.split()[1]
            self.data.setAdapter(adapter)




    self.fid.close()

if __name__=="__main__":
    myParser = gravitTimeParser()
    myParser.parseFile("../tests/t_4.out")
    myParser.printRunInfo()



    # numThreads = myParser.getNumThreads()
    # adapter = myParser.getAdapter()
    # scheduler = myParser.getScheduler()

   #scheduler,tracerPart
