"""
AUTHOR: M. Montgomery 
DATE:   12/05/2018
FILE:   day05.py 

PROMPT: 
--- Day 5: Alchemical Reduction ---

You've managed to sneak in to the prototype suit manufacturing lab. The Elves are making decent progress, but are still struggling with the suit's size reduction capabilities. While the very latest in 1518 alchemical technology might have solved their problem eventually, you can do better. You scan the chemical composition of the suit's material and discover that it is formed by extremely long polymers (one of which is available as your puzzle input).

The polymer is formed by smaller units which, when triggered, react with each other such that two adjacent units of the same type and opposite polarity are destroyed. Units' types are represented by letters; units' polarity is represented by capitalization. For instance, r and R are units with the same type but opposite polarity, whereas r and s are entirely different types and do not react.

For example:
    In aA, a and A react, leaving nothing behind.
    In abBA, bB destroys itself, leaving aA. As above, this then destroys itself, leaving nothing.
    In abAB, no two adjacent units are of the same type, and so nothing happens.
    In aabAAB, even though aa and AA are of the same type, their polarities match, and so nothing happens.

Now, consider a larger example, dabAcCaCBAcCcaDA:

dabAcCaCBAcCcaDA  The first 'cC' is removed.
dabAaCBAcCcaDA    This creates 'Aa', which is removed.
dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
dabCBAcaDA        No further actions can be taken.

After all possible reactions, the resulting polymer contains 10 units. How many units remain after fully reacting the polymer you scanned?

--- Part Two ---

Time to improve the polymer.

One of the unit types is causing problems; it's preventing the polymer from collapsing as much as it should. Your goal is to figure out which unit type is causing the most problems, remove all instances of it (regardless of polarity), fully react the remaining polymer, and measure its length.

For example, again using the polymer dabAcCaCBAcCcaDA from above:

    Removing all A/a units produces dbcCCBcCcD. Fully reacting this polymer produces dbCBcD, which has length 6.
    Removing all B/b units produces daAcCaCAcCcaDA. Fully reacting this polymer produces daCAcaDA, which has length 8.
    Removing all C/c units produces dabAaBAaDA. Fully reacting this polymer produces daDA, which has length 4.
    Removing all D/d units produces abAcCaCBAcCcaA. Fully reacting this polymer produces abCBAc, which has length 6.

In this example, removing all C/c units was best, producing the answer 4. What is the length of the shortest polymer you can produce by removing all units of exactly one type and fully reacting the result?
"""

import sys


def findRemainingUnits(polymer):
    """ Destroys all reactive pairs in given polymer until no more reactions
        can occur; returns length of resulting polymer. """

    toCheck = 0
    while toCheck < len(polymer) - 1:
        
        # remove current and next element if they'll be destroyed
        if willDestroy(polymer[toCheck], polymer[toCheck+1]):
            polymer.pop(toCheck)
            polymer.pop(toCheck)

            # move back to check previous element w new neighbor
            if toCheck > 0:
                toCheck -= 1

        # otherwise, increment index from which to check
        else:
            toCheck += 1

    return len(polymer)
    

def willDestroy(left, right):
    """ Determines whether or not given characters are equivalent letters
        but different cases. """
    
    return left.upper() == right.upper() and left != right


def findFewestUnits(polymer):
    """ Determines the shortest possible length of the reacted polymer
        if a single letter may be entirely removed first (both cases). """

    # get all letters used
    letters = set()
    for char in polymer:
        letters.add(char.upper())

    # find shortest reacted polymer
    shortest = float('inf')
    for letter in letters:

        # try removing a letter (both cases)
        newPolymer = polymer.replace(letter, '')
        newPolymer = newPolymer.replace(letter.lower(), '')

        # save reacted polymer length if shortest so far
        shortest = min(shortest, findRemainingUnits(list(newPolymer)))
        
    return shortest


def main():

    # get input
    polymer = sys.stdin.readline().strip()

    # PART ONE
    remainingUnits = findRemainingUnits(list(polymer))
    print("There are", remainingUnits, "units remaining in the reacted polymer.")

    # PART TWO
    fewestUnits = findFewestUnits(polymer)
    print("The shortest reacted polymer has", fewestUnits, "units.")
    

if __name__ == "__main__":
    main()
