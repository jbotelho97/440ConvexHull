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
	x3 = x
	x4 = x
	px = ((x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / \
		 float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
	py = ((x1*y2 - y1*x2)*(y3-y4) - (y1 - y2)*(x3*y4 - y3*x4)) / \
			float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3-x4))
	return py #Since we only use the y-value from yint() i removed the x-value return

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
	pointlen = len(points) - 1 #Used for quicksort
	points = quickSort(points, 0, pointlen) #Sorts by x-value
	# The helper recursion function, we dont want to keep calling quicksort so we  do this in another method
	points = computeHelper(points)
	clockwiseSort(points)
	return points

#The main function recurses until we reach the base case of n<=5 then brute forces the small hulls
# and merges the bigger hulls
def computeHelper(points):

	#Base Case
	if len(points) <= 5:
		return naiveHull(points)

	left = []
	right = []

	#We find the mean x-value of the points and then use that to sort the values in points into two lists
	#We do this so two lists don't contain a points with the same x-value
	mean = (points[0][0] + points[len(points) - 1][0]) / 2

	#Work-in-progress on an edge case where one part of the list is just a straight vertical line
	if points[0][0] == points[len(points) - 1][0]:
		return points

	#While there is still points for the loops to loop through it will compare them to the mean
	# if they are less then or equal to the mean they go in the left list, otherwise the go in the right list
	for i in range(len(points)):
		if points[i][0] <= mean:
			left.append(points[i])
		else:
			right.append(points[i])
	#recursive step
	left = computeHelper(left)
	right = computeHelper(right)

	#After recursion we begin merging
	return mergeHulls(left, right)

#Quicksort Algorithm slighty tweeked to work with out list of tuples. I took this off a website and mad eit work for our tuples
# https://www.geeksforgeeks.org/python-program-for-quicksort/ <- Source for the code
#It is only called once in the entire program at the begining, we just need sorting to do the splits
def quickSort(arr, low, high):
	if low < high:

		pi = quickPart(arr, low, high)

		quickSort(arr, low, pi - 1)
		quickSort(arr, pi + 1, high)
	return arr
#partition for quicksort
def quickPart(arr, low, high):
	i = low - 1
	pivot = arr[high]

	for j in range(low, high):
		if arr[j][0] <= pivot[0]:
			i += 1
			arr[i],arr[j] = arr[j],arr[i]

	arr[i+1],arr[high] = arr[high],arr[i+1]

	return (i+1)
#modular addition
def moda(a, size):
	return (a + 1) % size
#modular subtraction
def mods(a, size):
	return (a - 1) % size
#the meat of the program, this merges two convex hulls into a singular one
def mergeHulls(left, right):

	#This came up in tests but if one list is empty we return the other list
	if len(left) == 0:
		return right
	if len(right) == 0:
		return left

	#These hold the length of the left and right lists
	leftSize = len(left)
	rightSize = len(right)

	#A clockwise sort to get them in clockwise order(although as Prof. Daniels pointed out this actually sorts in
	#counter-clockwise order
	clockwiseSort(left)
	clockwiseSort(right)

	#Finding the furthest right value in the left list
	leftMax = left[0][0] #Maximum x-value of the left
	li = 0 #Index of said maximum
	for i in range(len(left)):
		if left[i][0] > leftMax:
			leftMax = left[i][0]
			li = i #index of highist x-value of left list


	#Finding the furthest left value of the right list
	rightMin = right[0][0]  # Maximum x-value of the left
	ri = 0  # Index of said maximum
	for i in range(len(right)):
		if right[i][0] < rightMin:
			rightMin = right[i][0]
			ri = i#index of the lowest x-value of the right list


	divder = (leftMax + rightMin) / 2 #Line L to calculate the y-intercept

	#Values for yint
	ymin = -100000000 #This number might need to be bigger if you are dealing with over 100,000,000 entries
	ymax = -ymin

	#Upper Tangent
	indexL = li #Sets the index to the rightmost point in the left list
	indexR = ri #Sets the index to the leftmost point in the right list
	done = False
	#Invarient: While list is not done we will continue to move the left index counter clockwise and the right index clockwise
	#until the upper tangent is found
	#Maintenence: We check that when the loop is iterated through the values of indexL and indexR are actually changing
	#Termination: Upper bound has been found, values of indexL and indexR won't change so the loop will terminate
	while not done:
		startL = indexL
		startR = indexR
		while yint(left[mods(indexL, leftSize)], right[indexR], divder, ymin, ymax) < yint(left[indexL], right[indexR], divder, ymin, ymax):
			indexL = mods(indexL, leftSize)
		while yint(left[indexL], right[moda(indexR, rightSize)], divder, ymin, ymax) < yint(left[indexL], right[indexR], divder, ymin, ymax):
			indexR = moda(indexR, rightSize)
		if startL == indexL and startR == indexR: #If the values have not changes through a loop iteration, terminate
			done = True

	#Stores the index of the upper bound
	upperL = indexL
	upperR = indexR

	#Reset indexL and indexR so we can do the same loop but for the lower bound
	indexL = li
	indexR = ri
	# Invarient: While list is not done we will continue to move the left index clockwise and the right index counter-clockwise
	# until the lower tangent is found
	# Maintenence: We check that when the loop is iterated through the values of indexL and indexR are actually changing
	# Termination: Lower bound has been found, values of indexL and indexR won't change so the loop will terminate
	done = False
	while not done:
		startL = indexL
		startR = indexR
		while yint(left[moda(indexL, leftSize)], right[indexR], divder, ymin, ymax) > yint(left[indexL], right[indexR], divder, ymin, ymax):
			indexL = moda(indexL, leftSize)
		while yint(left[indexL], right[mods(indexR, rightSize)], divder, ymin, ymax) > yint(left[indexL], right[indexR], divder, ymin, ymax):
			indexR = mods(indexR, rightSize)
		if startL == indexL and startR == indexR:
			done = True

	#Holds the indicies of the lower bound
	lowerL = indexL
	lowerR = indexR

	combinedHull = []#holds the combined hull

	#Combining Lists
	#left list
	#Invariant: While ine index has not reached the variable lowerL, all points it goes over are in the hull
	#Maintenence: We decrease the index to move counter-clockwise through the list checking every time that it is not lowerL
	#Termination: We reach lowerL meaning all further points are no longer in the hull
	ind = upperL
	combinedHull.append(left[upperL])
	while ind != lowerL:#This will go through the list counter-clockwise until it reaches the lower tangent on the left list
		ind = (ind - 1) % leftSize
		combinedHull.append(left[ind])
	#right List
	#Invariant: While ine index has not reached the variable upperR, all points it goes over are in the hull
	#Maintenence: We decrease the index to move counter-clockwise through the list checking every time that it is not upperR
	#Termination: We reach upperR meaning all further points are no longer in the hull
	ind = lowerR
	combinedHull.append(right[lowerR])
	while ind != upperR: #This will go through the list counter-clockwise until it reaches the upper tangent on the right list
		ind = (ind - 1) % rightSize
		combinedHull.append(right[ind])
	return combinedHull

#Simple naive brute force sort when n = 5
def naiveHull(points):
	p = points;
	listl = len(p)

	if listl <= 3: #Any three or less points will always constitute the hull
		return points

	hull = [];
	#Invariant: While there exists an element in list p that has not been tested to see if itis on the hull yet, the
	# loop will continue
	#Maintenence: The loop will increment up the list checking every single element
	#Termination: When the end of the list is reached every element will have been tested to see if it is on the hull
	for i in range(len(p)):
		j = (i + 1) % listl
		#Invariant: While there a exists a line segment (i,j) that has not been tested to see if all points lie to one side of it
		# the loop will continue checking all possible line segments
		#Maintenence: The loop will modularly increment j while making sure it is not equal to i
		#Termination: All possible combinations of (i,j) have been tested and the point i is either in the hull or not
		while j != i:
			k = (j + 1) % listl
			for count in range(listl - 2): #does n-2 comparisons checking if all points are on the side of line
				if k == i:
					k = (k + 1) % listl
				cwR = cw(p[i], p[j], p[k]) #True is those three points form a clockwise motion
				if not cwR:
					cwR = collinear(p[i], p[j], p[k])#checks if those points are colinear
					if not cwR:#This means the points tested are clockwise
						break#If they are clockwise we move to the next line segment
				k = (k + 1) % listl
			if cwR:
				hull.append(p[i])#If all points can be found clockwise to some point and line segment add to hull
				break
			j = (j + 1) % listl

	return hull;


#Testing Function
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