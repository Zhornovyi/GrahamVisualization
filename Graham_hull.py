import numpy
from matplotlib import pyplot as plt # for plotting
from random import randint # for sorting and creating data pts
from math import atan2 # for computing polar angle
from numpy import arccos, array, dot, pi, cross
from numpy.linalg import det, norm
from polylabel import polylabel


def create_points(ct,min=0,max=100):
	return [[randint(min,max),randint(min,max)] \
			for _ in range(ct)]

def scatter_plot(coords,convex_hull=None,centr = None):
	xs,ys=zip(*coords) # unzip into x and y coord lists
	plt.scatter(xs,ys) # plot the data points

	if convex_hull!=None:
		for i in range(1,len(convex_hull)+1):
			if i==len(convex_hull): i=0 # wrap
			c0=convex_hull[i-1]
			c1=convex_hull[i]
			plt.plot((c0[0],c1[0]),(c0[1],c1[1]),'r')
		circle = plt.Circle(centr[0], centr[1])
		ax = plt.gca()
		ax.add_patch(circle)
		plt.axis('scaled')
	plt.show()

def polar_angle(p0,p1=None):
	if p1==None: p1=anchor
	y_span=p0[1]-p1[1]
	x_span=p0[0]-p1[0]
	return atan2(y_span,x_span)

def distance(p0,p1=None):
	if p1==None: p1=anchor
	y_span=p0[1]-p1[1]
	x_span=p0[0]-p1[0]
	return y_span**2 + x_span**2

def det(p1,p2,p3):
	return   (p2[0]-p1[0])*(p3[1]-p1[1]) \
			-(p2[1]-p1[1])*(p3[0]-p1[0])

def quicksort(a):
	if len(a)<=1: return a
	smaller,equal,larger=[],[],[]
	piv_ang=polar_angle(a[randint(0,len(a)-1)]) # select random pivot
	for pt in a:
		pt_ang=polar_angle(pt) # calculate current point angle
		if   pt_ang<piv_ang:  smaller.append(pt)
		elif pt_ang==piv_ang: equal.append(pt)
		else: 				  larger.append(pt)
	return   quicksort(smaller) \
			+sorted(equal,key=distance) \
			+quicksort(larger)

def graham_scan(points,show_progress=False):
	global anchor
	min_idx=None
	for i,(x,y) in enumerate(points):
		if min_idx==None or y<points[min_idx][1]:
			min_idx=i
		if y==points[min_idx][1] and x<points[min_idx][0]:
			min_idx=i
	anchor=points[min_idx]

	sorted_pts=quicksort(points)
	del sorted_pts[sorted_pts.index(anchor)]

	hull=[anchor,sorted_pts[0]]
	for s in sorted_pts[1:]:
		while det(hull[-2],hull[-1],s)<=0:
			del hull[-1] # backtrack
			#if len(hull)<2: break
		hull.append(s)
		if show_progress: scatter_plot(points,hull)
	return hull

pts=create_points(20)
print ("Points:",pts)
hull=graham_scan(pts)
print ("Hull:",hull)
centr = polylabel([hull], with_distance=True)
scatter_plot(pts,hull,centr)