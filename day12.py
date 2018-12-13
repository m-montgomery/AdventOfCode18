"""
AUTHOR: M. Montgomery 
DATE:   12/12/2018
FILE:   day12.py 

PROMPT: 
--- Day 12: Subterranean Sustainability ---

The year 518 is significantly more underground than your history books implied. Either that, or you've arrived in a vast cavern network under the North Pole.

After exploring a little, you discover a long tunnel that contains a row of small pots as far as you can see to your left and right. A few of them contain plants - someone is trying to grow things in these geothermally-heated caves.

The pots are numbered, with 0 in front of you. To the left, the pots are numbered -1, -2, -3, and so on; to the right, 1, 2, 3.... Your puzzle input contains a list of pots from 0 to the right and whether they do (#) or do not (.) currently contain a plant, the initial state. (No other pots currently contain plants.) For example, an initial state of #..##.... indicates that pots 0, 3, and 4 currently contain plants.

Your puzzle input also contains some notes you find on a nearby table: someone has been trying to figure out how these plants spread to nearby pots. Based on the notes, for each generation of plants, a given pot has or does not have a plant based on whether that pot (and the two pots on either side of it) had a plant in the last generation. These are written as LLCRR => N, where L are pots to the left, C is the current pot being considered, R are the pots to the right, and N is whether the current pot will have a plant in the next generation. For example:

    A note like ..#.. => . means that a pot that contains a plant but with no plants within two pots of it will not have a plant in it during the next generation.
    A note like ##.## => . means that an empty pot with two plants on each side of it will remain empty in the next generation.
    A note like .##.# => # means that a pot has a plant in a given generation if, in the previous generation, there were plants in that pot, the one immediately to the left, and the one two pots to the right, but not in the ones immediately to the right and two to the left.

It's not clear what these plants are for, but you're sure it's important, so you'd like to make sure the current configuration of plants is sustainable by determining what will happen after 20 generations.

For example, given the following input:

initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #

For brevity, in this example, only the combinations which do produce a plant are listed. (Your input includes all possible combinations.) Then, the next 20 generations will look like this:

                 1         2         3     
       0         0         0         0     
 0: ...#..#.#..##......###...###...........
 1: ...#...#....#.....#..#..#..#...........
 2: ...##..##...##....#..#..#..##..........
 3: ..#.#...#..#.#....#..#..#...#..........
 4: ...#.#..#...#.#...#..#..##..##.........
 5: ....#...##...#.#..#..#...#...#.........
 6: ....##.#.#....#...#..##..##..##........
 7: ...#..###.#...##..#...#...#...#........
 8: ...#....##.#.#.#..##..##..##..##.......
 9: ...##..#..#####....#...#...#...#.......
10: ..#.#..#...#.##....##..##..##..##......
11: ...#...##...#.#...#.#...#...#...#......
12: ...##.#.#....#.#...#.#..##..##..##.....
13: ..#..###.#....#.#...#....#...#...#.....
14: ..#....##.#....#.#..##...##..##..##....
15: ..##..#..#.#....#....#..#.#...#...#....
16: .#.#..#...#.#...##...#...#.#..##..##...
17: ..#...##...#.#.#.#...##...#....#...#...
18: ..##.#.#....#####.#.#.#...##...##..##..
19: .#..###.#..#.#.#######.#.#.#..#.#...#..
20: .#....##....#####...#######....#.#..##.

The generation is shown along the left, where 0 is the initial state. The pot numbers are shown along the top, where 0 labels the center pot, negative-numbered pots extend to the left, and positive pots extend toward the right. Remember, the initial state begins at pot 0, which is not the leftmost pot used in this example.

After one generation, only seven plants remain. The one in pot 0 matched the rule looking for ..#.., the one in pot 4 matched the rule looking for .#.#., pot 9 matched .##.., and so on.

In this example, after 20 generations, the pots shown as # contain plants, the furthest left of which is pot -2, and the furthest right of which is pot 34. Adding up all the numbers of plant-containing pots after the 20th generation produces 325.

After 20 generations, what is the sum of the numbers of all pots which contain a plant?
"""

import sys, copy

def getCheckSum(initialState, rules, generations):
    """ Given a list of pots, the evolution rules, and the number of 
        generations, simulates the plant evolution and returns the
        check sum (as described in prompt). """

    plants = copy.deepcopy(initialState)
    zero = 0

    # simulate evolution over generations
    for _ in range(generations):
        plants, zero = evolve(plants, rules, zero)

    # calculate checksum
    checkSum = 0
    for i in range(zero, len(plants)):
        if plants[i] == "#":
            checkSum += i - zero
    for i in range(zero):       # negative-numbered pots
        if plants[i] == "#":
            checkSum -= zero - i

    return checkSum


def addPots(initialState, zero):
    """ Given a list of pots, prepends and appends empty pots as needed
        to ensure plants can grow infinitely in either direction. """

    # while there's a plant within 4 pots of either end of the list
    for i in range(4):

        # add an empty pot
        if initialState[i] == "#":
            initialState = ["."] + initialState
            zero += 1
        if initialState[-i] == "#":
            initialState += ["."]

    return initialState, zero


def evolve(initialState, rules, zero):
    """ Given a list of pots, the evolution rules, and the index of
        Pot #0, simulates one generation of evolution. """

    # add pots to ends JIC
    initialState, zero = addPots(initialState, zero)
    newState = ["."] * len(initialState)
    
    # determine evolved state
    for i in range(len(initialState)):
        try:
            newState[i] = rules[''.join(initialState[i-2:i+3])]
        except KeyError:
            newState[i] = "."

    # report new zero index
    return newState, zero

    
def main():

    # get input
    initialState = [x for x in sys.stdin.readline().strip().split(" ")[2:][0]]
    sys.stdin.readline()
    ruleInput = [line.strip() for line in sys.stdin.readlines()]

    # organize rules
    rules = {}
    for rule in ruleInput:
        parts = rule.split(" ")
        rules[parts[0]] = parts[2]

    # PART ONE
    checkSum = getCheckSum(initialState, rules, 20)
    print("After 20 generations:", checkSum)

    
    # PART TWO

    # determine linear factor
    # sums = {0:0}
    # diffs = []
    # for i in range(1, 200):
    #     sums[i] = getCheckSum(initialState, rules, i)
    #     diffs.append(sums[i] - sums[i-1])
        
    #     print("After {} generations:".format(i), sums[i],
    #           "\t diff from last:", diffs[-1])

    # linear factor determined to be: 65
    # first instance was after 109 generations, when there were 8041 plants
    
    print("After 50000000000 generations:",
          8041 + (65 * (50000000000 - 109)))

if __name__ == "__main__":
    main()
