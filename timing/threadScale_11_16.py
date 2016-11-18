
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


knlThreadCount=[1,2,4,8,10,17,34,67,68]
knlList=[]
for i in knlThreadCount:
  knlParser = gvtp.gravitTimeParser()
  knlParser.parseFile("../data/knl-dev/t_" + str(i) + ".out")
  knlList.append([i,knlParser])
  del knlParser

print "knl 1 thread filter times = ", knlList[0][1].data.getTracerDict()['filter']


x86ThreadCount = [1,2,4,5,10,15,19,20]

gpuList=[]
hasList=[]
for i in x86ThreadCount:
  gpuParser = gvtp.gravitTimeParser()
  gpuParser.parseFile("../data/mav-dev-gpu/t_" + str(i) + ".out")
  gpuList.append([i,gpuParser])
  del gpuParser
  hasParser = gvtp.gravitTimeParser()
  hasParser.parseFile("../data/mav-dev/t_" + str(i) + ".out")
  hasList.append([i,hasParser])
  del hasParser

print "Maverick total time array [ms] for 1 thread is ", hasList[0][1].getTotalTimeArray()

#now make tot time averages for each threadcount
knlTimePerThread=np.array([])
for i in range(0,len(knlThreadCount)):
     tmpTotTime=np.average(knlList[i][1].getTotalTimeArray()[1:])
     knlTimePerThread=np.append(knlTimePerThread,tmpTotTime)

hasTimePerThread=np.array([])
for i in range(0,len(x86ThreadCount)):
     tmpTotTime=np.average(hasList[i][1].getTotalTimeArray()[1:])
     hasTimePerThread=np.append(hasTimePerThread,tmpTotTime)

gpuTimePerThread=np.array([])
for i in range(0,len(x86ThreadCount)):
     tmpTotTime=np.average(gpuList[i][1].getTotalTimeArray()[1:])
     gpuTimePerThread=np.append(gpuTimePerThread,tmpTotTime)

#py.plot([x / x86ThreadCount[-1] for x in x86ThreadCount],gpuTimePerThread, '-bo')
py.plot(x86ThreadCount,gpuTimePerThread, '-bo',label='gpu')
py.plot(x86ThreadCount,hasTimePerThread,'-go',label='mav-haswell')
py.plot(knlThreadCount,knlTimePerThread,'-ro',label='knl')
py.xlabel('Thread count')
py.ylabel('Avg. Tracer Total time [ms]')
py.legend()
py.show()
