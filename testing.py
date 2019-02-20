#Testing File

import sys
from random import randint
from convexhull import computeHull


# argv takes a number randomly generates that many points
def main():
    if len(sys.argv) != 2:
        exit(1)

    numGen = int(sys.argv[1])

    points = []

    for i in range(numGen):
        randX = randint(0, 1000)
        randY = randint(0, 800)
        temp = [randX, randY]
        points.append(temp)

    answers = computeHull(points)

    for i in range(len(answers)):
        print("X: ", answers[i][0], " Y: ", answers[i][1], "\n")

    return 0

#necessary to work from the command line
if __name__ == '__main__':
    main()

