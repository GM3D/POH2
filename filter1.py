import sys
import itertools

int_ = int
len_ = len
imap = itertools.imap
product = itertools.product
split = str.split
find = str.find
append = list.append
extend = list.extend
sort = list.sort

def input_data():
    content = split(sys.stdin.read().rstrip(), '\n')
    H, W = imap(int_, split(content[0]))
    grid = content[1:H + 1]
    N = int_(content[H + 1])
    widgets = imap(lambda l: map(int_, split(l)), content[H + 2:])
    return (H, W, N, grid, widgets)

def print_data(H, W, N, grid, widgets):
    print "H, W = %d, %d" % (H, W)
    print "N = %d" % N
    print "grid:\n%s" % grid
    print "widgets:\n%s" % list(widgets)

def filter(h, w, i, j, H, W, grid):
    lines = grid[i:i + h]
    for line in lines:
        if find(line, '1', j, j + w) >= 0:
            return False
    return True

def filter_all(H, W, N, grid, widgets):
    locs = []
    for h, w in  widgets:
        count = 0
        for i, j in product(xrange(H - h + 1), xrange(W - w + 1)):
            if filter(h, w, i, j, H, W, grid):
                count += 1
        append(locs, count)
    return locs

if __name__ == '__main__':
    print '\n'.join(map(str, filter_all(*input_data())))
    #print_data(*input_data())
