
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
#1)create dict of timers for each file {run:'knl or gpu or haswell',
# 'thread count':numThreads,'data':tracerDict}

if __name__=="__main__":
    myParser = gvtp.gravitTimeParser()
    myParser.parseFile("../tests/t_4.out")
    myParser.printRunInfo()
    t4Filter=myParser.data.getTracerDict()['filter']
    print np.average(t4Filter[1:])
    print myParser.data.getNumTrials()
