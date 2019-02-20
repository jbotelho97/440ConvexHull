#Testing File

import sys
from random import randint
from convexhull import computeHull, insertion_sort, quickSort


# argv takes a number randomly generates that many points
def main():
    if len(sys.argv) != 2:
        exit(1)

    numGen = int(sys.argv[1])

    points = []

    # points.append([0, 0])
    # points.append([0, 3])
    # points.append([1, 1])
    # points.append([2, 0])
    #
    # numGen = len(points)

    for i in range(numGen):
        randX = randint(0, 10000000)
        randY = randint(0, 10000000)
        temp = (randX, randY)
        points.append(temp)


    answers = computeHull(points)
    # answers = quickSort(points,0,(numGen - 1))

    # for i in range(len(answers)):
    #     print("X: ", answers[i][0], " Y: ", answers[i][1], "\n")

    print("Input: ", numGen, "Output: ", len(answers),"\n")

    return 0

#necessary to work from the command line
if __name__ == '__main__':
    main()

