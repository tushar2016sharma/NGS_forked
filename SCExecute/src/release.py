#!/bin/env python
RELEASE = "SCExecute"
VERSION = '1.2.4'
PROGRAMS = 'scExecute.py scBAMStats.py minDepth.py'
INCLUDES = 'common'
if __name__ == '__main__':
    import sys
    print(eval(sys.argv[1]))
