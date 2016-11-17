import sys
import os
import os.path
import gzip
import getopt
import copy
import numpy as np



if __name__=="__main__":

  myParser = gravitTimeParser()
  myParser.parseFile("../tests/t_4.out")

  
