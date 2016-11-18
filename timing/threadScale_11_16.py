
#!/usr/bin/env python
import sys
import numpy as np
import matplotlib.pylab as py

sys.path.append('../modules')
try:
    import gvt_timing_parse as gvtp
except:
    print "could not files gvt_timing_parse module"



#needed
#1)create dict of timers for all {run:'knl or gpu or haswell',
# 'thread count':numThreads,'data':tracerDict,'trial count':numTrials}



myParser = gvtp.gravitTimeParser()
myParser.parseFile("../tests/t_4.out")
myParser.printRunInfo()
t4Filter=myParser.data.getTracerDict()['filter']
print np.average(t4Filter[1:])
print myParser.data.getNumTrials()


knlParser = gvtp.gravitTimeParser()
knlParser.parseFile("../data/knl-dev/t_1.out")
knlParser.printRunInfo()
scalingDict={'run':'knl','thread count':knlParser.data.getNumThreads(),
             'data':knlParser.data.getTracerDict(),
             'trial count':knlParser.data.getNumTrials()}
