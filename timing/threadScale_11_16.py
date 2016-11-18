
  1 #! /usr/bin/env python
  2
  3 import sys
  4 import numpy as np

sys.path.append('../modules')
 6 try:
 7   import cesmperftiming as cpt
 8 except:
 9   print "could not files cesmTimer module"

if __name__=="__main__":
    myParser = gravitTimeParser()
    myParser.parseFile("../tests/t_4.out")
    myParser.printRunInfo()
    t4Filter=myParser.data.getTracerDict()['filter']
    print np.average(t4Filter[1:])
    print myParser.data.getNumTrials()
