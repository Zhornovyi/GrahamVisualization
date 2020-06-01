import obj as obj
from matplotlib import pyplot as plt  # for plotting
from random import randint  # for sorting and creating data pts
from math import atan2  # for computing polar angle
from polylabel import polylabel, polylabel_
from matplotlib.animation import FuncAnimation
from centroid import centroid

fig = plt.figure()# create a figure
ax = fig.add_subplot(1,1,1)
centr2 = [0,0]

def create_points(ct, min=0, max=100): #generate random points
    return [[randint(min, max), randint(min, max)] \
            for _ in range(ct)]

def animate(convex_hull, points,centr=None): # for animation
    ax.clear() #clear figure each time when call  DELETE TO SHOW POLYLABEL WORK
    xs, ys = zip(*points)  # unzip into x and y coord lists
    ax.scatter(xs, ys)

    ax.scatter(centr2[0], centr2[1], color = 'red')
    plt.annotate("Centroid", (centr2[0], centr2[1]))

    if convex_hull != None: # add lines of the hull
        for i in range(1, len(convex_hull)):
            c0 = convex_hull[i - 1]
            c1 = convex_hull[i]
            ax.plot((c0[0], c1[0]), (c0[1], c1[1]), 'r')
    if centr != None: #add circle to plot
        ax.scatter(centr[0][0], centr[0][1], color='green')
        plt.annotate("Real centr", (centr[0][0], centr[0][1]))
        circle = plt.Circle(centr[0], centr[1], fill = False)
        ax1 = plt.gca()
        ax1.add_patch(circle)
        plt.axis('scaled')

def animete_PIO(cell): # animaton of searching the centr of circle
    rect = plt.Rectangle(xy=(cell.x, cell.y),width=cell.h, height=cell.h, fill = False)
    sub1 = plt.Rectangle(xy=(cell.x, cell.y),width=cell.h/2, height=cell.h/2, fill = False)
    sub2 = plt.Rectangle(xy=(cell.x+ cell.h/2, cell.y+cell.h/2),width=cell.h/2, height=cell.h/2, fill=False)
    plt.scatter(cell.x, cell.y, color='yellow')
    plt.gca().add_patch(rect)
    plt.gca().add_patch(sub1)
    plt.gca().add_patch(sub2)

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

def build_hull(anchor, sorted_pts) -> obj:
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

def build_hull_list(anchor, sorted_pts) -> obj:
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
def main():
    global centr2
    pts = create_points(10)
    print("Points:", pts)
    anchor, sorted_pts = graham_scan(pts)
    hull = build_hull_list(anchor, sorted_pts)
    centr = polylabel_([hull], with_distance = True)
    print(centr)
    centr2 = centroid(hull)
    print(centr2)
    ani = FuncAnimation(fig, animate, frames= build_hull(anchor,sorted_pts), fargs= (pts,centr), interval=100, repeat=False)
    #aniPIO = FuncAnimation(fig,animete_PIO, frames = polylabel([hull]), interval=100, repeat=False)
    plt.show()
if __name__ =="__main__":
    main()
