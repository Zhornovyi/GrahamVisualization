from random import randint  # for sorting and creating data pts
from math import atan2  # for computing polar angle

def create_points(ct, min=0, max=100): #generate random points
    return [[randint(min, max), randint(min, max)] \
            for _ in range(ct)]

def polar_angle(p0, p1=None): #calculate the polar angle
    if p1 == None: p1 = anchor
    y_span = p0[1] - p1[1]
    x_span = p0[0] - p1[0]
    return atan2(y_span, x_span)

def distance(p0, p1=None): # calculate distance between two points
    if p1 == None: p1 = anchor
    y_span = p0[1] - p1[1]
    x_span = p0[0] - p1[0]
    return y_span ** 2 + x_span ** 2

def deter(p1, p2, p3): # calculate deteminant of matrix
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) \
           - (p2[1] - p1[1]) * (p3[0] - p1[0])

def quicksort(list): # used to sort the points with increasing the polar angle
    if len(list) <= 1: return list
    smaller, equal, larger = [], [], []
    pivot_ang = polar_angle(list[randint(0, len(list) - 1)])  # select random pivot
    for point in list:
        point_angle = polar_angle(point)  # calculate current point angle
        if point_angle < pivot_ang:
            smaller.append(point)
        elif point_angle == pivot_ang:
            equal.append(point)
        else:
            larger.append(point)
    return quicksort(smaller) + sorted(equal, key=distance) + quicksort(larger)

def build_hull(anchor, sorted_pts):
    hull = [anchor, sorted_pts[0]]
    for s in sorted_pts[1:]:
        while deter(hull[-2], hull[-1], s) <= 0:
            subhull = [hull[-2],hull[-1],s]
            yield hull[0:len(hull)-1]+subhull
            del hull[-1]
        hull.append(s)
        yield hull
    hull.append(anchor)
    yield hull

def build_hull_list(anchor, sorted_pts):
    hull = [anchor, sorted_pts[0]]
    for s in sorted_pts[1:]:
        while deter(hull[-2], hull[-1], s) <= 0:
            del hull[-1]  # backtrack
        hull.append(s)
    return hull

def graham_scan(points, show_progress=False):
    global anchor
    min_idx = None
    for i, (x, y) in enumerate(points):
        if min_idx == None or y < points[min_idx][1]:
            min_idx = i
        if y == points[min_idx][1] and x < points[min_idx][0]:
            min_idx = i
    anchor = points[min_idx]

    sorted_pts = quicksort(points)
    del sorted_pts[sorted_pts.index(anchor)]
    return anchor,sorted_pts

