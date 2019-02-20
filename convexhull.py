import math
import sys

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
                - a[0]*c[1] + b[0]*c[1] - c[0]*b[1]) / 2.0;

'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a clockwise sequence
(subject to floating-point precision)
'''
def cw(a, b, c):
	return triangleArea(a,b,c) < EPSILON;
'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a counter-clockwise sequence
(subject to floating-point precision)
'''
def ccw(a, b, c):
	return triangleArea(a,b,c) > EPSILON;

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

	if len(points) <= 5:
		return naiveHull(points)

	left = []
	right = []

	points = insertion_sort(points)

	split = int(len(points) / 2)

	for i in range(split):
		left.append(points[i])

	for j in range(split, len(points)):
		right.append(points[j])

	left = computeHull(left)
	right = computeHull(right)

	return mergeHulls(left, right)

	# p = naiveHull(points);
	# return p;
	#return points;

def insertion_sort(arr):
	for i in range(len(arr)):
		cursor = arr[i]
		pos = i

		while pos > 0 and arr[pos - 1][0] > cursor[0]:
			# Swap the number down the list
			arr[pos] = arr[pos - 1]
			pos = pos - 1
		# Break and do the final swap
		arr[pos] = cursor

	return arr

def mergeHulls(left, right):

	leftSize = len(left)
	rightSize= len(right)

	#Finding the furthest right value in the left list
	leftMax = 0 #Maximum x-value of the left
	li = 0 #Index of said maximum
	for i in range(len(left)):
		if left[i][0] > leftMax:
			leftMax = left[i][0]
			li = i

	#Finding the furthest left value of the right list
	rightMin = 1000  # Maximum x-value of the left
	ri = 0  # Index of said maximum
	for i in range(len(right)):
		if right[i][0] < rightMin:
			rightMin = right[i][0]
			ri = i

	divder = (leftMax + rightMin) / 2

	#Uppoer Tangent
	indexL = li
	indexR = ri
	done = False
	upperT = yint(left[indexL], right[indexR], divder, 0, 800)
	upperT = upperT[1]
	while not done:
		startR = indexR
		startL = indexL
		indexR = (indexR + 1) % rightSize
		tempBound = yint(left[indexL], right[indexR], divder, 0, 800)
		if upperT >= tempBound[1]:
			upperT = tempBound[1]
		else:
			indexR = (indexR - 1) % rightSize

		indexL = (indexL - 1) % leftSize
		tempBound = yint(left[indexL], right[indexR], divder, 0, 800)
		if upperT >= tempBound[1]:
			upperT = tempBound[1]
		else:
			indexL = (indexL + 1) % leftSize

		#End-Case: if the loop has gone through with no changes to the indeicies
		if startL == indexL and startR == indexR:
			done = True

	upperL = indexL
	upperR = indexR

	#Lower Tangent
	indexL = li
	indexR = ri
	done = False
	lowerT = yint(left[indexL], right[indexR], divder, 0, 800)
	lowerT = lowerT[1]
	while not done:
		startR = indexR
		startL = indexL
		indexR = (indexR - 1) % rightSize
		tempBound = yint(left[indexL], right[indexR], divder, 0, 800)
		if lowerT <= tempBound[1]:
			lowerT = tempBound[1]
		else:
			indexR = (indexR + 1) % rightSize

		indexL = (indexL + 1) % leftSize
		tempBound = yint(left[indexL], right[indexR], divder, 0, 800)
		if lowerT <= tempBound[1]:
			lowerT = tempBound[1]
		else:
			indexL = (indexL - 1) % leftSize

		# End-Case: if the loop has gone through with no changes to the indeicies
		if startL == indexL and startR == indexR:
			done = True

	lowerL = indexL
	lowerR = indexR

	combinedHull = []

	#Combining Lists
	#left list
	ind = upperL
	combinedHull.append(left[upperL])
	while ind != lowerL:
		ind = (ind - 1) % leftSize
		combinedHull.append(left[ind])
	#right List
	ind = lowerR
	combinedHull.append(right[lowerR])
	while ind != upperR:
		ind = (ind - 1) % rightSize
		combinedHull.append(right[ind])

	clockwiseSort(combinedHull)

	return combinedHull

#Simple naive brute force sort when n = 5
def naiveHull(points):
	p = points;
	clockwiseSort(p);

	hull = [];

	for i in range(len(p)):
		j = (i + 1) % len(p);
		for j in range(len(p)):
			k = (j + 1) % len(p);
			test = 0
			for c in range(len(p)):
				if k == i or k == j:
					k = (k + 1) % len(p);
					continue
				# elif c == j or c == i:
				# 	c = (c + 1) % len(p)
				comp = triangleArea(p[i], p[j], p[k])
				if comp >= 0:
					test += 1
				else:
					test -= 1;
				k = (k + 1) % len(p);
			if abs(test) == (len(p) - 2):
				hull.append(p[i])
				break
	return hull;
