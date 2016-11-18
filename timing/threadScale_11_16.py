
#!/usr/bin/env python
import sys
import numpy as np
import matplotlib.pylab as py

sys.path.append('../modules')
try:
    import gvt_timing_parse as gvtp
except:
    print "could not files gvt_timing_parse module"




myParser = gvtp.gravitTimeParser()
myParser.parseFile("../tests/t_4.out")
myParser.printRunInfo()
t4Filter=myParser.data.getTracerDict()['filter']
print np.average(t4Filter[1:])
print myParser.data.getNumTrials()


knlParser = gvtp.gravitTimeParser()
knlThreadCount=[1,2,4,8,10,17,34,67,68]
knlList=[]
for i in knlThreadCount:
  knlParser.parseFile("../data/knl-dev/t_" + str(i) + ".out")
  knlList.append([i,knlParser.data])

print "knl 1 thread filter times = ", knlList[0][1].getTracerDict()['filter']

gpuParser = gvtp.gravitTimeParser()
hasParser = gvtp.gravitTimeParser()
x86ThreadCount = [1,2,4,5,10,15,19,20]

gpuList=[]
hasList=[]
for i in x86ThreadCount:
  gpuParser.parseFile("../data/mav-dev-gpu/t_" + str(i) + ".out")
  gpuList.append([i,gpuParser.data])
  hasParser.parseFile("../data/mav-dev/t_" + str(i) + ".out")
  hasList.append([i,hasParser.data])
