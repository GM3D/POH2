from datagen1 import *
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
        for data in dataset:
            p = subprocess.Popen(cmdline,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            printdata(data, file=p.stdin)
            pout, perr = p.communicate()
            p.stdin.close()
            r = p.poll()
            if r != 0:
                print "poll status: %s" % r
                print " %s didn't end correctly." % cmdline
                print "Child process error message: %s" % perr
                p.terminate()
            print "Child process output:\n%s "  % pout.rstrip()

    elif len(sys.argv) == 3:
        outputs = []
        for data in dataset:
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
                printdata(data, file=p.stdin)
                pout, perr = p.communicate()
                p.stdin.close()
                r = p.poll()
                if r != 0:
                    print "poll status: %s" % r
                    print " %s didn't end correctly." % cmdline
                    print "Child process error message: %s" % perr
                    p.terminate()
                outputs.append(pout.rstrip())
            assert compare_outputs(outputs, data)
    else:
        print("Usage: %s, prog1 [prog2]" % sys.argv[0])


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

if __name__ == '__main__':
    perform_test(100)
