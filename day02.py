"""
AUTHOR: M. Montgomery 
DATE:   12/02/2018
FILE:   day02.py 

PROMPT: 
--- Day 2: Inventory Management System ---

You stop falling through time, catch your breath, and check the screen on the device. "Destination reached. Current Year: 1518. Current Location: North Pole Utility Closet 83N10." You made it! Now, to find those anomalies.

Outside the utility closet, you hear footsteps and a voice. "...I'm not sure either. But now that so many people have chimneys, maybe he could sneak in that way?" Another voice responds, "Actually, we've been working on a new kind of suit that would let him fit through tight spaces like that. But, I heard that a few days ago, they lost the prototype fabric, the design plans, everything! Nobody on the team can even seem to remember important details of the project!"

"Wouldn't they have had enough fabric to fill several boxes in the warehouse? They'd be stored together, so the box IDs should be similar. Too bad it would take forever to search the warehouse for two similar box IDs..." They walk too far away to hear any more.

Late at night, you sneak to the warehouse - who knows what kinds of paradoxes you could cause if you were discovered - and use your fancy wrist device to quickly scan every box and produce a list of the likely candidates (your puzzle input).

To make sure you didn't miss any, you scan the likely candidate boxes again, counting the number that have an ID containing exactly two of any letter and then separately counting those with exactly three of any letter. You can multiply those two counts together to get a rudimentary checksum and compare it to what your device predicts.

For example, if you see the following box IDs:

    abcdef contains no letters that appear exactly two or three times.
    bababc contains two a and three b, so it counts for both.
    abbcde contains two b, but no letter appears exactly three times.
    abcccd contains three c, but no letter appears exactly two times.
    aabcdd contains two a and two d, but it only counts once.
    abcdee contains two e.
    ababab contains three a and three b, but it only counts once.

Of these box IDs, four of them contain a letter which appears exactly twice, and three of them contain a letter which appears exactly three times. Multiplying these together produces a checksum of 4 * 3 = 12.

What is the checksum for your list of box IDs?

--- Part Two ---

Confident that your list of box IDs is complete, you're ready to find the boxes full of prototype fabric. The boxes will have IDs which differ by exactly one character at the same position in both strings. For example, given the following box IDs:

abcde, fghij, klmno, pqrst, fguij, axcye, wvxyz

The IDs abcde and axcye are close, but they differ by two characters (the second and fourth). However, the IDs fghij and fguij differ by exactly one character, the third (h and u). Those must be the correct boxes.

What letters are common between the two correct box IDs? (In the example above, this is found by removing the differing character from either ID, producing fgij.)
"""

import sys

def findChecksum(boxIDs):
    """ Returns the checksum as described in prompt, given list of box IDs. """

    containsTwo   = 0   # number of boxes w 2-letter count
    containsThree = 0   # number of boxes w 3-letter count

    # for every box ID
    for box in boxIDs:

        # check if box contains 2 or 3 letter-counts
        counts = countLetters(box)
        if 2 in counts:
            containsTwo += 1
        if 3 in counts:
            containsThree += 1

    # return product for checksum
    return containsTwo * containsThree


def countLetters(ID):
    """ Returns a set of letter counts for an ID. """

    counts = set()
    for letter in ID:
        counts.add(ID.count(letter))
    return counts


def findCommonID(boxIDs):
    """ Returns the common letters of the 2 IDs that are only 1 letter apart,
        given list of box IDs. """

    # for every pair of IDs
    for i in range(len(boxIDs) - 1):
        for j in range(i, len(boxIDs)):

            # check their differences
            diff = 0
            A = boxIDs[i]
            B = boxIDs[j]
            for p in range(len(A)):

                # found a difference
                if A[p] != B[p]:
                    diff += 1

                # stop looking if more than 1 apart
                if diff > 1:
                    break

            # if only 1 apart, return their common letters
            if diff == 1:
                return getCommonLetters(A, B)

    return ""


def getCommonLetters(A, B):
    """ Returns only the letters that are in the same places in A and B. """

    ans = ""
    for i in range(len(A)):
        if A[i] == B[i]:
            ans += A[i]
    return ans
    
    
def main():

    # get input
    boxIDs = [line.strip() for line in sys.stdin.readlines()]

    # PART ONE
    checksum = findChecksum(boxIDs)
    print("The checksum is:", checksum)

    # PART TWO
    commonID = findCommonID(boxIDs)
    print("The common ID is:", commonID)
    

if __name__ == "__main__":
    main()
