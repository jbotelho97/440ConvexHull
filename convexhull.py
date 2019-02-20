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
		xr = x1
		return (xr, yr)
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
	# points = insertion_sort(points)
	# points = computeHelper(points)
	points = naiveHull(points)
	clockwiseSort(points)
	return points

def computeHelper(points):

	if len(points) <= 5:
		return naiveHull(points)

	points = insertion_sort(points)

	left = []
	right = []

	split = int(len(points) / 2)

	for i in range(split):
		left.append(points[i])

	for j in range(split, len(points)):
		right.append(points[j])

	left = computeHelper(left)
	right = computeHelper(right)

	return mergeHulls(left, right)

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

	#Checking if edge points have the same x-value
	def compare(lefti, righti):
		return left[lefti] == right[righti]


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

	# combinedHull = clockwiseSort(combinedHull)

#	print("Size: ", len(combinedHull), "\n")

	return combinedHull

#Simple naive brute force sort when n = 5
def naiveHull(points):
	p = points;
	clockwiseSort(p);

	hull = [];

	for i in range(len(p)):
		jStart = (i + 1) % len(p);
		for j in range(jStart, len(p)):
			k = (j + 1) % len(p);
			test = 0
			for c in range(len(p)):
				if k == i or k == j:
					k = (k + 1) % len(p);
					continue
				#comp = triangleArea(p[i], p[j], p[k])
				colin = collinear(p[i], p[j], p[k])
				clock = cw(p[i],p[j],p[k])
				if clock:
					test += 1
				elif not clock:
					test -= 1;
				else:
					if test >= 0:
						test += 1
					else:
						test -= 1
				k = (k + 1) % len(p);
			if abs(test) == (len(p) - 2):
				hull.append(p[i])
				break
	return hull;

def checkHull(hull, points):
	points = naiveHull(points)
	same = True
	insertion_sort(points)
	insertion_sort(hull)
	assert(len(points) == len(hull))
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