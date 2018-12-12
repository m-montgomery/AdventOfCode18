"""
AUTHOR: M. Montgomery 
DATE:   12/11/2018
FILE:   day11.py 

PROMPT: 
--- Day 11: Chronal Charge ---

You watch the Elves and their sleigh fade into the distance as they head toward the North Pole. Actually, you're the one fading. The falling sensation returns.

The low fuel warning light is illuminated on your wrist-mounted device. Tapping it once causes it to project a hologram of the situation: a 300x300 grid of fuel cells and their current power levels, some negative. You're not sure what negative power means in the context of time travel, but it can't be good.

Each fuel cell has a coordinate ranging from 1 to 300 in both the X (horizontal) and Y (vertical) direction. In X,Y notation, the top-left cell is 1,1, and the top-right cell is 300,1. The interface lets you select any 3x3 square of fuel cells. To increase your chances of getting to your destination, you decide to choose the 3x3 square with the largest total power.

The power level in a given fuel cell can be found through the following process:

Find the fuel cell's rack ID, which is its X coordinate plus 10. Begin with a power level of the rack ID times the Y coordinate. Increase the power level by the value of the grid serial number (your puzzle input). Set the power level to itself multiplied by the rack ID. Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0). Subtract 5 from the power level.

For example, to find the power level of the fuel cell at 3,5 in a grid with serial number 8:

    The rack ID is 3 + 10 = 13.
    The power level starts at 13 * 5 = 65.
    Adding the serial number produces 65 + 8 = 73.
    Multiplying by the rack ID produces 73 * 13 = 949.
    The hundreds digit of 949 is 9.
    Subtracting 5 produces 9 - 5 = 4.

So, the power level of this fuel cell is 4.

Your goal is to find the 3x3 square which has the largest total power. The square must be entirely within the 300x300 grid. Identify this square using the X,Y coordinate of its top-left fuel cell. What is the X,Y coordinate of the top-left fuel cell of the 3x3 square with the largest total power?

--- Part Two ---

You discover a dial on the side of the device; it seems to let you select a square of any size, not just 3x3. Sizes from 1x1 to 300x300 are supported. Realizing this, you now must find the square of any size with the largest total power. Identify this square by including its size as a third parameter after the top-left coordinate: a 9x9 square with a top-left corner of 3,5 is identified as 3,5,9.

For example:

For grid serial number 18, the largest total square (with a total power of 113) is 16x16 and has a top-left corner of 90,269, so its identifier is 90,269,16. For grid serial number 42, the largest total square (with a total power of 119) is 12x12 and has a top-left corner of 232,251, so its identifier is 232,251,12.

What is the X,Y,size identifier of the square with the largest total power?
"""

import sys

def makeGrid(SN):
    """ Given a serial number, returns a 300x300 grid of power values
        calculated according to prompt. """

    # initialize grid size (300x300)
    grid = [[0] * 300 for _ in range(300)]

    # for every spot (cell) in grid
    for y in range(1, 301):
        for x in range(1, 301):

            # calculate fuel cell's power level
            rackID = x + 10
            power = ((rackID * y) + SN) * rackID
            power = -5 if power < 100 else int(str(power)[-3]) - 5

            # add cell to grid
            grid[y-1][x-1] = power

    return grid


def getLargest3x3(grid):
    """ Given a grid of power values, returns the upper lefthand coordinate
        of the 3x3 square with the largest sum of power values. """
    
    highX = 0     # upper left-hand X
    highY = 0     # upper left-hand Y
    highest = 0   # square sum

    # find largest sum of 3x3 squares
    for y in range(298):
        for x in range(298):

            # calculate sum of current square
            local = 0
            for i in range(3):
                for j in range(3):
                    local += grid[y+i][x+j]

            # save values if higher sum
            if local > highest:
                highest = local
                highX = x + 1
                highY = y + 1

    return highX, highY


def getLargestSquare(grid):
    """ Given a grid of power values, returns the upper lefthand coordinate
        and the size of the square with the largest sum of power values. """

    highX = 0     # upper left-hand X
    highY = 0     # upper left-hand Y
    highSize = 0  # size of the square
    highest = 0   # largest square sum

    # initialize sum grid size (301x301 for ease)
    sums = [[0] * 301 for _ in range(301)]

    # create summation grid
    for y in range(1, 301):
        for x in range(1, 301):
            sums[y][x] = grid[y-1][x-1] + \
                         sums[y-1][x]   + \
                         sums[y]  [x-1] - \
                         sums[y-1][x-1]

    # find largest sum
    for size in range(1, 301):
        for y in range(size, 301):
            for x in range(size, 301):

                # get local sum
                local = sums[y]     [x]      - \
                        sums[y-size][x]      - \
                        sums[y]     [x-size] + \
                        sums[y-size][x-size]

                # save values if higher sum
                if local > highest:
                    highest = local
                    highX = x - size + 1
                    highY = y - size + 1
                    highSize = size

    return highX, highY, highSize
    

def main():

    # get input
    SN = int(sys.stdin.readline().strip())
    grid = makeGrid(SN)

    # PART ONE
    coord = getLargest3x3(grid)
    print("UL coordinate:", coord)

    # PART TWO
    x, y, size = getLargestSquare(grid)
    print("UL coordinate:", (x, y), "- Square size:", size)

    
if __name__ == "__main__":
    main()
