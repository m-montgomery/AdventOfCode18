"""
AUTHOR: M. Montgomery 
DATE:   12/08/2018
FILE:   day07.py 

PROMPT: 
--- Day 7: The Sum of Its Parts ---

You find yourself standing on a snow-covered coastline; apparently, you landed a little off course. The region is too hilly to see the North Pole from here, but you do spot some Elves that seem to be trying to unpack something that washed ashore. It's quite cold out, so you decide to risk creating a paradox by asking them for directions.

"Oh, are you the search party?" Somehow, you can understand whatever Elves from the year 1018 speak; you assume it's Ancient Nordic Elvish. Could the device on your wrist also be a translator? "Those clothes don't look very warm; take this." They hand you a heavy coat.

"We do need to find our way back to the North Pole, but we have higher priorities at the moment. You see, believe it or not, this box contains something that will solve all of Santa's transportation problems - at least, that's what it looks like from the pictures in the instructions." It doesn't seem like they can read whatever language it's in, but you can: "Sleigh kit. Some assembly required."

"'Sleigh'? What a wonderful name! You must help us assemble this 'sleigh' at once!" They start excitedly pulling more parts out of the box.

The instructions specify a series of steps and requirements about which steps must be finished before others can begin (your puzzle input). Each step is designated by a single letter. For example, suppose you have the following instructions:

Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.

Visually, these requirements look like this:


  -->A--->B--
 /    \      \
C      -->D----->E
 \           /
  ---->F-----

Your first goal is to determine the order in which the steps should be completed. If more than one step is ready, choose the step which is first alphabetically. In this example, the steps would be completed as follows:

Only C is available, and so it is done first. Next, both A and F are available. A is first alphabetically, so it is done next. Then, even though F was available earlier, steps B and D are now also available, and B is the first alphabetically of the three. After that, only D and F are available. E is not available because only some of its prerequisites are complete. Therefore, D is completed next. F is the only choice, so it is done next. Finally, E is completed.

So, in this example, the correct order is CABDFE. In what order should the steps in your instructions be completed?

--- Part Two ---

As you're about to begin construction, four of the Elves offer to help. "The sun will set soon; it'll go faster if we work together." Now, you need to account for multiple people working on steps simultaneously. If multiple steps are available, workers should still begin them in alphabetical order.

Each step takes 60 seconds plus an amount corresponding to its letter: A=1, B=2, C=3, and so on. So, step A takes 60+1=61 seconds, while step Z takes 60+26=86 seconds. No time is required between steps.

To simplify things for the example, however, suppose you only have help from one Elf (a total of two workers) and that each step takes 60 fewer seconds (so that step A takes 1 second and step Z takes 26 seconds). Then, using the same instructions as above, this is how each second would be spent:

Second   Worker 1   Worker 2   Done
   0        C          .        
   1        C          .        
   2        C          .        
   3        A          F       C
   4        B          F       CA
   5        B          F       CA
   6        D          F       CAB
   7        D          F       CAB
   8        D          F       CAB
   9        D          .       CABF
  10        E          .       CABFD
  11        E          .       CABFD
  12        E          .       CABFD
  13        E          .       CABFD
  14        E          .       CABFD
  15        .          .       CABFDE

Each row represents one second of time. The Second column identifies how many seconds have passed as of the beginning of that second. Each worker column shows the step that worker is currently doing (or . if they are idle). The Done column shows completed steps.

Note that the order of the steps has changed; this is because steps now take time to finish and multiple workers can begin multiple steps simultaneously. In this example, it would take 15 seconds for two workers to complete these steps.

With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?
"""

import sys, re, copy


def extractPairs(instructions):

    Rpair = re.compile("Step (\w) must be finished before step (\w) can begin.")
    
    pairs = []
    for line in instructions:
        data = Rpair.search(line)
        if data:
            pairs.append((data.group(1), data.group(2)))
    return pairs


def makeDependencies(IDs, pairs):

    dependencies = {}
    for ID in IDs:
        dependencies[ID] = []
    for A, B in pairs:
        dependencies[A] += [B]
    return dependencies


def determineOrder(IDs, dependencies):

    queue = []
    order = []

    # until every step is in the order
    while len(order) != len(IDs):

        # evaluate each remaining step
        for step in dependencies:
            if step in queue or step in order:
                continue

            # check if still dependent on another step
            available = True
            for other in dependencies:
                if step in dependencies[other]:
                    available = False

            if available:
                queue.append(step)

        # add first step in sorted queue to order
        queue.sort()
        order.append(queue[0])

        # release step's dependents
        del dependencies[queue.pop(0)]

    return ''.join(order)
    

def determineTimedOrder(IDs, dependencies):

    queue = []
    order = []
    inProgress = []

    # set up for timing tasks
    timings = {}
    for ID in IDs:
        timings[ID] = ord(ID) - 4   # ord 'A' is 65; needs to be 61
    time = 0
    NWORKERS = 5

    # until every step is in the order
    while len(order) != len(IDs):

        # evaluate each remaining step
        for step in dependencies:
            if step in queue or step in inProgress:
                continue

            # check if still dependent on another step
            available = True
            for other in dependencies:
                if step in dependencies[other]:
                    available = False

            if available:
                queue.append(step)

        # move steps from sorted queue to in-progress
        queue.sort()
        while len(inProgress) < NWORKERS and len(queue) > 0:
            inProgress.append(queue.pop(0))

        # work on each available step
        working = min(NWORKERS, len(inProgress))
        for i in range(working-1, -1, -1):

            # reduce time remaining by 1
            step = inProgress[i]
            timings[step] -= 1

            # completed a step
            if timings[step] == 0:

                # move step from in-progress to order
                order.append(step)
                inProgress.pop(i)

                # release step's dependents
                del dependencies[step]

        time += 1

    return ''.join(order), time


def main():

    # get input
    lines = [line.strip() for line in sys.stdin.readlines()]
    pairs = extractPairs(lines)
    IDs = set()
    for A, B in pairs:
        IDs.add(A)
        IDs.add(B)
    dependencies = makeDependencies(IDs, pairs)

    # PART ONE
    order = determineOrder(IDs, copy.deepcopy(dependencies))
    print("Order:    ", order)

    # PART TWO
    order, time = determineTimedOrder(IDs, dependencies)
    print("New order:", order, "(", time, "seconds )")

    
if __name__ == "__main__":
    main()
