"""
AUTHOR: M. Montgomery 
DATE:   12/03/2018
FILE:   day03.py 

PROMPT: 
--- Day 3: No Matter How You Slice It ---

The Elves managed to locate the chimney-squeeze prototype fabric for Santa's suit (thanks to someone who helpfully wrote its box IDs on the wall of the warehouse in the middle of the night). Unfortunately, anomalies are still affecting them - nobody can even agree on how to cut the fabric.

The whole piece of fabric they're working on is a very large square - at least 1000 inches on each side. Each Elf has made a claim about which area of fabric would be ideal for Santa's suit. All claims have an ID and consist of a single rectangle with edges parallel to the edges of the fabric. Each claim's rectangle is defined as follows:

The number of inches between the left edge of the fabric and the left edge of the rectangle; The number of inches between the top edge of the fabric and the top edge of the rectangle; The width of the rectangle in inches; The height of the rectangle in inches. 

A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge, 2 inches from the top edge, 5 inches wide, and 4 inches tall. Visually, it claims the square inches of fabric represented by # (and ignores the square inches of fabric represented by .) in the diagram below:

...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........

The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas. For example, consider the following claims:

#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2

Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........

The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others, does not overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric are within two or more claims?

--- Part Two ---

Amidst the chaos, you notice that exactly one claim doesn't overlap by even a single square inch of fabric with any other claim. If you can somehow draw attention to it, maybe the Elves will be able to make Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims are made.

What is the ID of the only claim that doesn't overlap?
"""

import re, sys


def processClaim(fabric, overlapped, claim):
    """ Adds a claim to a fabric grid that tracks number of claims on each
        spot in the grid and IDs of previous claims. """

    ID, x, y, width, height = claim

    # add rows as needed
    while y + height > len(fabric):
        fabric.append([[0,-1]] * len(fabric[0]))

    # add cols as needed
    for i in range(len(fabric)):
        while x + width > len(fabric[i]):
            fabric[i].append([0,-1])

    # visit every spot in claim on fabric
    for i in range(y, y + height):
        for j in range(x, x + width):

            # mark if overlapping another claim
            count, prevID = fabric[i][j]
            if count != 0:
                overlapped[prevID] = 1
                overlapped[ID - 1] = 1  # IDs start at 1, indices start at 0

            # update claim count for spot
            fabric[i][j] = [count + 1, ID - 1]


def findOverlapping(fabric):
    """ Tallies the overlapping square inches given a fabric grid. """

    total = 0
    for row in fabric:
        for spot in row:
            if spot[0] > 1:
                total += 1

    return total


def findNotOverlapped(overlapped):
    """ Locates the ID of the claim unmarked for overlapping. """

    for i in range(len(overlapped)):
        if overlapped[i] == 0:
            return i + 1
        
    return 0


def main():

    # get input
    claims = [line.strip() for line in sys.stdin.readlines()]
    
    # define fabric grid and claim format
    fabric = [[]]
    overlapped = []
    claimRE = re.compile("^#(\\d+) @ (\\d+),(\\d+): (\\d+)x(\\d+)$")

    # process each claim
    for claim in claims:

        # extract values from claim and process
        result = claimRE.match(claim)
        if result:
            overlapped.append(0)
            processClaim(fabric, overlapped,
                         [int(result.group(i)) for i in range(1,6)])

    # PART ONE
    # tally overlapping claims
    print("There are {} square inches of fabric "
          "with one or more claims.".format(findOverlapping(fabric)))

    # PART TWO
    # report non-overlapped claim
    print("Claim #{} is not overlapping any other claim."
          "".format(findNotOverlapped(overlapped)))
    
    
if __name__ == "__main__":
    main()
