
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
knlMinTimePerThread=np.array([])
knlStdPerThread=np.array([])
for i in range(0,len(knlThreadCount)):
     tmpTotTime=np.average(knlList[i][1].getTotalTimeArray()[1:])
     tmpMinTotTime=np.amin(knlList[i][1].getTotalTimeArray()[1:])
     tmpTotStd=np.std(knlList[i][1].getTotalTimeArray()[1:])
     knlTimePerThread=np.append(knlTimePerThread,tmpTotTime)
     knlMinTimePerThread=np.append(knlMinTimePerThread,tmpMinTotTime)
     knlStdPerThread=np.append(knlStdPerThread,tmpTotStd)

hasTimePerThread=np.array([])
hasMinTimePerThread=np.array([])
hasStdPerThread=np.array([])
for i in range(0,len(x86ThreadCount)):
     tmpTotTime=np.average(hasList[i][1].getTotalTimeArray()[1:])
     tmpMinTotTime=np.amin(hasList[i][1].getTotalTimeArray()[1:])
     tmpTotStd=np.std(hasList[i][1].getTotalTimeArray()[1:])
     hasTimePerThread=np.append(hasTimePerThread,tmpTotTime)
     hasMinTimePerThread=np.append(hasMinTimePerThread,tmpMinTotTime)
     hasStdPerThread=np.append(hasStdPerThread,tmpTotTime)

gpuTimePerThread=np.array([])
gpuMinTimePerThread=np.array([])
gpuStdPerThread=np.array([])
for i in range(0,len(x86ThreadCount)):
     tmpTotTime=np.average(gpuList[i][1].getTotalTimeArray()[1:])
     tmpMinTotTime=np.amin(gpuList[i][1].getTotalTimeArray()[1:])
     tmpTotStd=np.std(gpuList[i][1].getTotalTimeArray()[1:])
     gpuTimePerThread=np.append(gpuTimePerThread,tmpTotTime)
     gpuMinTimePerThread=np.append(gpuMinTimePerThread,tmpMinTotTime)
     gpuStdPerThread=np.append(gpuStdPerThread,tmpTotTime)

print "knlStd = ",knlStdPerThread
print "hasStd = ",hasStdPerThread
print "gpuStd = ",gpuStdPerThread

fig1=py.figure(1)
ax1=py.subplot(211)
ax1.set_yscale("log", nonposy='clip')
py.errorbar(x86ThreadCount,gpuTimePerThread,yerr=gpuStdPerThread,fmt='-bo',label='gpu')
py.errorbar(x86ThreadCount,hasTimePerThread,yerr=hasStdPerThread,fmt='-go',label='mav-haswell')
py.errorbar(knlThreadCount,knlTimePerThread,yerr=knlStdPerThread,fmt='-ro',label='knl')
py.xlabel('Thread count')
py.ylabel('[Log] Avg. Tracer Total time [ms]')
py.legend()


# ax2=py.subplot(312)
# ax2.set_yscale("log", nonposy='clip')
# py.errorbar(x86ThreadCount,gpuTimePerThread,yerr=gpuStdPerThread,fmt='-bo',label='gpu')
# py.errorbar(x86ThreadCount,hasTimePerThread,yerr=hasStdPerThread,fmt='-go',label='mav-haswell')
# #py.plot(knlThreadCount,knlTimePerThread,'-ro',label='knl')
# py.errorbar(knlThreadCount,knlTimePerThread,yerr=knlStdPerThread,fmt='-ro',label='knl')
# py.xlabel('Thread count')
# py.ylabel('[Log] Avg. Tracer Total time [ms]')
# py.legend()

#py.figure(2)
ax3=py.subplot(212)

ax3.set_yscale("log", nonposy='clip')
ax3.set_xscale("linear", nonposy='clip')
py.plot([x / float(knlThreadCount[-1]) for x in knlThreadCount],knlMinTimePerThread,'-ro',label='knl')
py.plot([x / float(x86ThreadCount[-1]) for x in x86ThreadCount],gpuMinTimePerThread,'-bo',label='gpu')
py.plot([x / float(x86ThreadCount[-1]) for x in x86ThreadCount],hasMinTimePerThread,'-go',label='mav-haswell')
py.xlabel('Node saturation')
py.ylabel('[Log] Min. Tracer Total time [ms]')
py.legend()

fig1.suptitle('gvtPly, 10 iterations, single mpi rank')

py.show()
