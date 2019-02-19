import math
import sys
import random
from hullGUI import *

EPSILON = sys.float_info.epsilon

'''
Given two points, p1 and p2,
an x coordinate, x,
and y coordinates y3 and y4,
compute and return the (x,y) coordinates
of the y intercept of the line segment p1->p2
with the line segment (x,y3)->(x,y4)
'''
def yint(p1, p2, x, y3, y4):
	x1, y1 = p1
	x2, y2 = p2
	x3 = x
	x4 = x
	px = ((x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / \
		 float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
	py = ((x1*y2 - y1*x2)*(y3-y4) - (y1 - y2)*(x3*y4 - y3*x4)) / \
			float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3-x4))
	return (px, py)

'''
Given three points a,b,c,
computes and returns the area defined by the triangle
a,b,c. 
Note that this area will be negative 
if a,b,c represents a clockwise sequence,
positive if it is counter-clockwise,
and zero if the points are collinear.
'''
def triangleArea(a, b, c):
	return (a[0]*b[1] - a[1]*b[0] + a[1]*c[0] \
                - a[0]*c[1] + b[0]*c[1] - c[0]*b[1]) / 2.0

'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a clockwise sequence
(subject to floating-point precision)
'''
def cw(a, b, c):
	return triangleArea(a,b,c) < EPSILON
'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a counter-clockwise sequence
(subject to floating-point precision)
'''
def ccw(a, b, c):
	return triangleArea(a,b,c) > EPSILON

'''
Given three points a,b,c,
returns True if and only if 
a,b,c are collinear
(subject to floating-point precision)
'''
def collinear(a, b, c):
	return abs(triangleArea(a,b,c)) <= EPSILON

'''
Given a list of points,
sort those points in clockwise order
about their centroid.
Note: this function modifies its argument.
'''
def clockwiseSort(points):
	# get mean x coord, mean y coord
	xavg = sum(p[0] for p in points) / len(points)
	yavg = sum(p[1] for p in points) / len(points)
	angle = lambda p:  ((math.atan2(p[1] - yavg, p[0] - xavg) + 2*math.pi) % (2*math.pi))
	points.sort(key = angle)

'''
Replace the implementation of computeHull with a correct computation of the convex hull
using the divide-and-conquer algorithm
'''
def computeHull(points):

	#Sort by x value
	sorted(points , key=lambda k: [k[0], k[1]])
	return computeHullHelper(points)

	

#Helper for computeHull
def computeHullHelper(points):
	if len(points) > 5:

		#Recurse on halves
		half = len(points)//2
		p1 = computeHull(points[:half])
		p2 = computeHull(points[half:])

		#Merge
		return mergeHull(p1, p2)

	else:
		return naiveHull(points)

#Merge Hulls
def mergeHull():

	intercept = yint(p1, p2, canvas_width/2, 0, canvas_hight)

	i = 1
	j = 1
	while (yint(p1[i],   p2[j+1], canvas_width/2, 0, canvas_hight) >
		   yint(p1[i],   p2[j],   canvas_width/2, 0, canvas_hight) or
		   yint(p1[i-1], p2[j],   canvas_width/2, 0, canvas_hight) >
		   yint(p1[i],   p2[j],   canvas_width/2, 0, canvas_hight)):

		if yint(p1[i],   p2[j+1], canvas_width/2, 0, canvas_hight) >
		   yint(p1[i],   p2[j],   canvas_width/2, 0, canvas_hight): #move right finger clockwise
			j = j+1 % len(p1)
		else:
			i = i - 1 % len(p2)
	return #something

#Naive Convex Hull Alg
def naiveComputeHUll(points):
	return 0

def maxPoint(points):
	xmax = max(p[0] for p in points)
	return xmax

def minPoint(points):
	xmin = min(p[0] for p in points)
	return xmin