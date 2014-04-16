from __future__ import print_function
import sys, random

def datagen1(h, w, n, occupancy=0.5):
    grid = []
    for i in xrange(h):
        l = []
        for j in xrange(w):
            x = random.random()
            l.append(int(x < occupancy))
        grid.append(l)
    widgets = []
    for i in xrange(n):
        s = random.randint(1, h)
        t = random.randint(1, w)
        widgets.append([s, t])
    return grid, widgets

def printdata(data, file=sys.stdout):
    grid, widgets = data
    h, w = len(grid), len(grid[0])
    n = len(widgets)
    print ("%d %d" % (h, w), file=file)
    for d in grid:
        print (''.join(map(str, d)), file=file)
    print ("%d" % n, file=file)
    for widget in widgets:
        print (' '.join(map(str, widget)), file=file)

if __name__ == '__main__':
    data = datagen1(4, 3, 3)
    printdata(data)
