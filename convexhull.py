import math
import sys
from hypothesis import given
import hypothesis.strategies as st

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
	if x1 == x2:
		yr = ((y1 + y2) / 2)
		return yr
	x3 = x
	x4 = x
	px = ((x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / \
		 float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
	py = ((x1*y2 - y1*x2)*(y3-y4) - (y1 - y2)*(x3*y4 - y3*x4)) / \
			float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3-x4))
	return int(py)

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
	return triangleArea(a,b,c) < -EPSILON;
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
	pointlen = len(points) - 1
	points = quickSort(points, 0, pointlen)
	points = computeHelper(points)
	# points = naiveHull(points)
	clockwiseSort(points)
	return points

def computeHelper(points):


	if len(points) <= 5:
		return naiveHull(points)

	left = []
	right = []

	# split = int(len(points) / 2)
	#
	# for i in range(split):
	# 	left.append(points[i])
	#
	# for j in range(split, len(points)):
	# 	right.append(points[j])

	mean = (points[0][0] + points[len(points) - 1][0]) / 2
	for i in range(len(points)):
		if points[i][0] <= mean:
			left.append(points[i])
		else:
			right.append(points[i])

	left = computeHelper(left)
	right = computeHelper(right)

	return mergeHulls(left, right)

def quickSort(arr, low, high):
	if low < high:

		pi = quickPart(arr, low, high)

		quickSort(arr, low, pi - 1)
		quickSort(arr, pi + 1, high)
	return arr

def quickPart(arr, low, high):
	i = low - 1
	pivot = arr[high]

	for j in range(low, high):
		if arr[j][0] <= pivot[0]:
			i += 1
			arr[i],arr[j] = arr[j],arr[i]

	arr[i+1],arr[high] = arr[high],arr[i+1]

	return (i+1)

def mergeHulls(left, right):

	if len(left) == 0:
		return right
	if len(right) == 0:
		return left
	leftSize = len(left)
	rightSize = len(right)

	clockwiseSort(left)
	clockwiseSort(right)

	#Finding the furthest right value in the left list
	leftMax = 0 #Maximum x-value of the left
	li = 0 #Index of said maximum
	for i in range(len(left)):
		if left[i][0] > leftMax:
			leftMax = left[i][0]
			li = i #index of highist x-value of left list


	#Finding the furthest left value of the right list
	rightMin = 1000  # Maximum x-value of the left
	ri = 0  # Index of said maximum
	for i in range(len(right)):
		if right[i][0] < rightMin:
			rightMin = right[i][0]
			ri = i#index of the lowest x-value of the right list


	divder = (leftMax + rightMin) / 2 #Line L to calculate the y-intercept

	#upper tangent
	indexL = li
	indexR = ri


	while yint(left[indexL], right[(indexR + 1) % rightSize], divder, 0, 800) < yint(left[indexL], right[indexR], divder, 0, 800) or \
			yint(left[(indexL - 1) % leftSize], right[indexR], divder, 0, 800) < yint(left[indexL], right[indexR], divder, 0, 800):
		if yint(left[indexL], right[(indexR + 1) % rightSize], divder, 0, 800) < yint(left[indexL], right[indexR], divder, 0, 800):
			indexR = (indexR + 1) % rightSize
		else:
			indexL = (indexL - 1) % leftSize


	upperL = indexL
	upperR = indexR

	indexL = li
	indexR = ri

	while yint(left[indexL], right[(indexR - 1) % rightSize], divder, 0, 800) > yint(left[indexL], right[indexR], divder, 0, 800) or \
			yint(left[(indexL + 1) % leftSize], right[indexR], divder, 0, 800) > yint(left[indexL], right[indexR], divder, 0, 800):
		if yint(left[indexL], right[(indexR - 1) % rightSize], divder, 0, 800) > yint(left[indexL], right[indexR], divder, 0, 800):
			indexR = (indexR - 1) % rightSize
		else:
			indexL = (indexL + 1) % leftSize

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

	return combinedHull

#Simple naive brute force sort when n = 5
def naiveHull(points):
	p = points;
	listl = len(p)

	if listl <= 3:
		return points

	hull = [];

	for i in range(len(p)):
		j = (i + 1) % listl
		while j != i:
			k = (j + 1) % listl
			for count in range(listl - 2): #does n-2 comparisons checking if all points are on the side of line
				if k == i:
					k = (k + 1) % listl
				cwR = cw(p[i], p[j], p[k])
				if not cwR:
					cwR = collinear(p[i], p[j], p[k])
					if not cwR:
						break
				k = (k + 1) % listl
			if cwR:
				hull.append(p[i])
				break
			j = (j + 1) % listl

	return hull;

def checkHull(hull, points):
	points = naiveHull(points)
	same = True
	clockwiseSort(points)
	clockwiseSort(hull)
	if len(points) != len(hull):
		print("Hull: ", len(hull), " Naive: ", len(points), "\n")
		return False
	for i in range(len(points)):
		if hull[i][0] != points[i][0] or hull[i][1] != points[i][1]:
			same = False
	return same

@given(
    st.lists(st.tuples(st.integers(0,1000000), st.integers(0,1000000)), 3, None, None, True)
)
def test_hull(points):
    hull = computeHull(points)
    assert checkHull(hull, points)

if __name__ == "__main__":
    test_hull()