import sys
import itertools

int_ = int
len_ = len
imap = itertools.imap
split = str.split
append = list.append
extend = list.extend
sort = list.sort

def input_data():
    content = split(sys.stdin.read().rstrip(), '\n')
    print "content:\n%s" % content
    H, W = imap(int_, split(content[0]))
    grid = content[1:H + 1]
    N = int_(content[H + 1])
    widgets = imap(lambda l: map(int_, split(l)), content[H + 2:])
    return H, W, N, grid, widgets

def print_data(H, W, N, grid, widgets):
    print "H, W = %d, %d" % (H, W)
    print "N = %d" % N
    print "grid:\n%s" % grid
    print "widgets:\n%s" % list(widgets)

if __name__ == '__main__':
    print_data(*input_data())
