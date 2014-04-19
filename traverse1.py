from __future__ import print_function

import copy
import sys
import itertools

int_ = int
len_ = len
imap = itertools.imap
prod = itertools.product
split = str.split
find = str.find
append = list.append
extend = list.extend
sort = list.sort

def debug_print(*args):
    if debug_print.debug:
        print(*args)

def input_data():
    content = split(sys.stdin.read().rstrip(), '\n')
    H, W = imap(int_, split(content[0]))
    grid = content[1:H + 1]
    N = int_(content[H + 1])
    widgets = list(imap(lambda l: tuple(map(int_, split(l))), content[H + 2:]))
    return (H, W, N, grid, widgets)

def print_data(H, W, N, grid, widgets):
    print("H, W = %d, %d, H * W = %d" % (H, W, H * W))
    print("N = %d" % N)
    # print("grid:\n%s" % grid)
    # print("widgets:\n%s" % list(widgets))

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


def get_next(unexplored):
    shape = unexplored[0]
    get_next.last_shape = shape
    get_next.last_was_ancillary = False if shape in unexplored else True
    if not get_next.last_was_ancillary:
        unexplored.remove(shape)
    return shape

get_next.last_shape = (1, 1)
get_next.last_was_ancillary = False


def init_white_list(H, W, grid):
    r = {}
    r[(1, 1)] = [(i, j) for (i, j) in prod(xrange(H), xrange(W)) 
                 if grid[i][j] == '0']
    return r

def make_white_list(H, W, N, grid, widgets):
    unexplored = copy.deepcopy(widgets)
    white_list = init_white_list(H, W, grid)
    while unexplored:
        debug_print("unexplored = ", unexplored)
        shape = get_next(unexplored)
        update(H, W, grid, white_list, shape)
    return white_list

def min_shape(unexplored):
    return (min((x[0] for x in unexplored)), min((x[1] for x in unexplored)))

def update(H, W, grid, white_list, shape):
    hint = find_smaller(shape, white_list)
    debug_print("hint = %s, shape = %s" % (hint, shape))
    update_using(H, W, grid, white_list, shape, hint)

def update_using(H, W, grid, white_list, shape, hint):
    def occupied(loc):
        i, j = loc
        return grid[i][j] == '1'
    h, w = shape
    h0, w0 = hint
    l0 = white_list[hint]
    l = []
    for loc in l0:
        i, j = loc
        if i + h - 1 < H and j + w - 1 < W:
            debug_print("checking loc", loc)
            if any(imap(occupied, ((i1, j1) for (i1, j1) in 
                                   prod(xrange(i, i + h0), 
                                        xrange(j + w0, j + w))))):
                debug_print("1st test failed")
                continue
            if any(imap(occupied, ((i1, j1) for (i1, j1) in 
                                   prod(xrange(i+h0, i + h), 
                                        xrange(j, j + w))))):
                debug_print("2nd test failed")
                continue
            append(l, loc)
    white_list[shape] = l


def d(shape1, shape2):
    return abs(shape2[0] - shape1[0]) + abs(shape2[1] - shape1[1])

def find_smaller(shape, white_list):
    debug_print("shape = %s, white_list = %s" % (shape, white_list))
    smaller = [shape1 for shape1 in white_list 
               if shape1[0] <= shape[0] and shape1[1] <= shape[1]]
    debug_print("smaller list = %s" % smaller)
    r = min(smaller, key=lambda s: d(s, shape))
    assert r != None
    return r

def output(white_list, H, W, N, grid, widgets):
    for widget in widgets:
        print(len(white_list[widget]))

if __name__ == '__main__':
    debug_print.debug = False
    data = input_data()
#    wdict = make_wdict(*data)
    white_list = make_white_list(*data)
    debug_print("white_list = %s" % white_list)
    output(white_list, *data)
#    debug_print( wdict
    # debug_print( "wdict entries = %d " % len(wdict.viewkeys())
    # debug_print( "length of each entries: %s" % stats(wdict)
