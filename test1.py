from datagen1 import *
from datetime import datetime, timedelta
import subprocess

def gen_dataset(times):
    dataset = []
    for i in xrange(times):
        h = random.randint(1, 130)
        w = random.randint(1, 130)
        n = random.randint(1, h * w)
        dataset.append(datagen1(h, w, n))
    return dataset

def perform_test(times):
    dataset = gen_dataset(times)
    if len(sys.argv) == 2:
        prog = sys.argv[1]
        if prog.endswith('.py'):
            cmdline = ['/usr/bin/python', prog]
        else:
            cmdline = [prog]
        print("peforming test of %s" % cmdline)
        ndata = len(dataset)
        idata = 0
        intervals = []
        for data in dataset:
            print("data %d of %d" % (idata, ndata))
            print_data_info(data)
            p = subprocess.Popen(cmdline,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            print("starting %s..." % prog)
            start = datetime.now()
            printdata(data, file=p.stdin)
            pout, perr = p.communicate()
            p.stdin.close()
            r = p.poll()
            if r != 0:
                print "poll status: %s" % r
                print " %s didn't end correctly." % cmdline
                print "Child process error message: %s" % perr
                p.terminate()
            end = datetime.now()
            print("%s terminated." % prog)
            print "Child process output:\n%s "  % pout.rstrip()
            intervals.append(end - start)
            idata += 1
    elif len(sys.argv) == 3:
        outputs = []
        ndata = len(dataset)
        idata = 0
        intervals = [[], []]
        for data in dataset:
            print("data %d of %d" % (idata, ndata))
            print_data_info(data)
            for i in (1, 2):
                prog = sys.argv[i]
                if prog.endswith('.py'):
                    cmdline = ('/usr/bin/python', prog)
                else:
                    cmdline = (prog)
                p = subprocess.Popen(cmdline,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
                print("starting %s..." % prog)
                start = datetime.now()
                printdata(data, file=p.stdin)
                pout, perr = p.communicate()
                p.stdin.close()
                r = p.poll()
                if r != 0:
                    print "poll status: %s" % r
                    print " %s didn't end correctly." % cmdline
                    print "Child process error message: %s" % perr
                    p.terminate()
                end = datetime.now()
                print("%s terminated." % prog)
                intervals[i - 1].append(end - start)
                outputs.append(pout.rstrip())
            assert compare_outputs(outputs, data)
            idata += 1
    else:
        print("Usage: %s, prog1 [prog2]" % sys.argv[0])
    report_interval(intervals)


def compare_outputs(outputs, data):
    o1 = outputs[0].split('\n')
    o2 = outputs[1].split('\n')
    # print "output[0]:\n", output[0]
    # print "output[1]:\n", output[1]
    for i in xrange(len(o1)):
        if not o1[i] == o2[i]:
            print "differs: o1[%d] = %s, o2[%d] = %s" % (i, o1[i], i, o2[i])
            with open("error_data.txt", 'wt') as f:
                printdata(data, file=f)
            return False
    return True

def print_data_info(data):
    grid, widgets = data
    H = len(grid)
    W = len(grid[0])
    N = len(widgets)
    print("(H, W, N) = (%d, %d, %d)" % (H, W, N))

def report_interval(intervals):
    if type(intervals[0]) == timedelta:
        n = len(intervals)
        i = 0
        print("execute time:")
        for t in intervals:
            print("data %d: %f" % ( i, t.seconds + 0.001 * t.microseconds))
            i += 1
    elif type(intervals[0]) == list:
        n = len(intervals[0])
        i = 0
        for t1, t2 in zip(intervals[0], intervals[1]):
            print("data %d: prog1: %f, prog2: %f" % 
                  (i, t1.seconds + 0.001 * t1.microseconds,
                   t2.seconds + 0.001 * t2.microseconds))
            i += 1
if __name__ == '__main__':
    perform_test(5)
