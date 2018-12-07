"""
AUTHOR: M. Montgomery 
DATE:   12/06/2018
FILE:   day06.py 

PROMPT: 
--- Day 6: Chronal Coordinates ---

The device on your wrist beeps several times, and once again you feel like you're falling. "Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual. If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate). Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9

If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.

This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each location's closest coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf

Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any. In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?

--- Part Two ---

On the other hand, if the coordinates are safe, maybe the best you can do is try to find a region near as many coordinates as possible.

For example, suppose you want the sum of the Manhattan distance to all of the coordinates to be less than 32. For each location, add up the distances to all of the given coordinates; if the total of those distances is less than 32, that location is within the desired region. Using the same coordinates as above, the resulting region looks like this:

..........
.A........
..........
...###..C.
..#D###...
..###E#...
.B.###....
..........
..........
........F.

This region, which also includes coordinates D and E, has a total size of 16.

Your actual region will need to be much larger than this example, though, instead including all locations with a total distance of less than 10000. What is the size of the region containing all locations which have a total distance to all given coordinates of less than 10000?
"""

import sys


def getLargestArea(coords):
    """ Given list of coordinates """

    # calculate boundaries
    maxX = max(x for [x,y] in coords)
    maxY = max(y for [x,y] in coords)
    minX = min(x for [x,y] in coords)
    minY = min(y for [x,y] in coords)
    
    # build grid
    grid = []
    for y in range(maxY+1):
        grid.append([0] * (maxX+1))

    # calculate closest points
    for y in range(len(grid)):
        for x in range(len(grid[y])):

            # skip areas leading to infinity
            if x <= minX or x >= maxX or y <= minY or y >= maxY:
                continue

            # save closest point in spot (None if tied)
            grid[y][x] = getClosestPoint(x, y, coords)

    # find the largest area
    area = 0
    for x,y in coords:
        
        # skip points with infinite areas
        if x in (minX, maxX) or y in (minY, maxY):
            continue

        area = max(area, getArea((x,y), grid))
    
    return area


def getClosestPoint(ptx, pty, coords):
    """ Given a point and a list of coordinates, finds the closest point. 
        Returns the closest coordinates or None if tied. """
    
    # calculate distances
    distance = {}
    for x, y in coords:
        distance[(x,y)] = abs(x - ptx) + abs(y - pty)

    # find closest
    smallest = min(distance.values())
    points = [pt for pt in distance if distance[pt] == smallest]
    return points[0] if len(points) == 1 else None


def getArea(pt, grid):
    """ Given coordinates and a grid, returns the area that the
        given point commands (i.e. spots closest to this point). """

    area = 0    
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == pt:
                area += 1
    return area           


def getSafeArea(coords):
    """ Given a list of coordinates, calculates the number of spots within a
        safe distance of every point (where total distance < 10000). """

    # get boundaries
    maxX = max(x for [x,y] in coords)
    maxY = max(y for [x,y] in coords)    

    # calculate each spot's total distance
    safeSpots = 0
    for y in range(maxY+1):
        for x in range(maxX+1):
            total = 0

            # calculate distance from each point
            for ptx, pty in coords:
                total += abs(x - ptx) + abs(y - pty)

            # safe if within 10000 total
            if total < 10000:
                safeSpots += 1

    return safeSpots
    

def main():

    # get input as x,y integers
    coords = []
    for coord in [line.strip() for line in sys.stdin.readlines()]:
        comma = coord.index(",")
        coords.append((int(coord[:comma]), int(coord[comma+2:])))
        
    # PART ONE
    area = getLargestArea(coords)
    print("The largest finite area is", area)

    # PART TWO
    safeArea = getSafeArea(coords)
    print("The safe region has an area of", safeArea)
    

if __name__ == "__main__":
    main()
