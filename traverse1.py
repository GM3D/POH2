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
    print "H, W = %d, %d, H * W = %d" % (H, W, H * W)
    print "N = %d" % N
    # print "grid:\n%s" % grid
    # print "widgets:\n%s" % list(widgets)

def make_wdict(H, W, N, grid, widgets):
    wdict = {}
    for widget in widgets:
        h, w = widget
        if h not in wdict:
            wdict[h] = [w]
        else:
            if w not in wdict[h]:
                wdict[h].append(w)
    for h in wdict:
        sort(wdict[h])
    return wdict
    
def stats(wdict):
    return [len(wdict[h]) for h in wdict]

if __name__ == '__main__':
    data = input_data()
    print_data(*data)
    wdict = make_wdict(*data)
#    print wdict
    print "wdict entries = %d " % len(wdict.viewkeys())
    print "length of each entries: %s" % stats(wdict)
