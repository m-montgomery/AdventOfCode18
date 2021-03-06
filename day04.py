"""
AUTHOR: M. Montgomery 
DATE:   12/04/2018
FILE:   day04.py 

PROMPT: 
--- Day 4: Repose Record ---

You've sneaked into another supply closet - this time, it's across from the prototype suit manufacturing lab. You need to sneak inside and fix the issues with the suit, but there's a guard stationed outside the lab, so this is as close as you can safely get.

As you search the closet for anything that might help, you discover that you're not the first person to want to sneak in. Covering the walls, someone has spent an hour starting every midnight for the past few months secretly observing this guard post! They've been writing down the ID of the one guard on duty that night - the Elves seem to have decided that one guard was enough for the overnight shift - as well as when they fall asleep or wake up while at their post (your puzzle input).

For example, consider the following records, which have already been organized into chronological order:

[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up

Timestamps are written using year-month-day hour:minute format. The guard falling asleep or waking up is always the one whose shift most recently started. Because all asleep/awake times are during the midnight hour (00:00 - 00:59), only the minute portion (00 - 59) is relevant for those events.

Note that guards count as asleep on the minute they fall asleep, and they count as awake on the minute they wake up. For example, because Guard #10 wakes up at 00:25 on 1518-11-01, minute 25 is marked as awake.

If you can figure out the guard most likely to be asleep at a specific time, you might be able to trick that guard into working tonight so you can have the best chance of sneaking in. You have two strategies for choosing the best guard/minute combination.

Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?

In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5), while Guard #99 only slept for a total of 30 minutes (10+10+10). Guard #10 was asleep most during minute 24 (on two days, whereas any other minute the guard was asleep was only seen on one day).

While this example listed the entries in chronological order, your entries are in the order you found them. You'll need to organize them before they can be analyzed.

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 10 * 24 = 240.)

--- Part Two ---

Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

In the example above, Guard #99 spent minute 45 asleep more than any other guard or minute - three times in total. (In all other cases, any guard spent any minute asleep at most twice.)

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 99 * 45 = 4455.)
"""

import re, sys


def main():

    # get input
    lines = [line.strip() for line in sys.stdin.readlines()]
    
    # define regex for processing the input
    RDateTime = re.compile("\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\]")
    RBegin    = re.compile("Guard #(\d+) begins shift")
    RSleep    = re.compile("falls asleep")
    RAwake    = re.compile("wakes up")

    # separate date/time from action in each line
    for i in range(len(lines)):
        line = lines[i]

        # extract date/time
        lineDateTime = RDateTime.search(line)
        if not lineDateTime:
            print("Couldn't find a date in this line:", line)
            continue

        # store date/time and action
        lines[i] = [[int(lineDateTime.group(j)) for j in range(1,6)],
                    line[lineDateTime.span()[1]+1:]]

    # sort actions by date/time
    sortedLines = sorted(lines, key=lambda x:x[0])

    # calculate sleep schedules for each guard
    guardSleepCounts = {}
    currentGuard = None
    lastSleptMin = None
    for date, line in sortedLines:

        # save current guard number
        lineGuard = RBegin.search(line)
        if lineGuard:
            currentGuard = int(lineGuard.group(1))

        # save minute when fell asleep
        elif RSleep.search(line):
            if currentGuard not in guardSleepCounts:
                guardSleepCounts[currentGuard] = [0] * 60
            lastSleptMin = date[-1]

        # increment counts of minutes asleep
        elif RAwake.search(line):
            awokenMin = date[-1]
            for i in range(lastSleptMin, awokenMin):
                guardSleepCounts[currentGuard][i] += 1

    # PART ONE
                
    # find guard who slept the most
    highest = 0
    chosenGuard = None
    for guard in guardSleepCounts:

        # look for a sum with higher count
        minutesSlept = sum(guardSleepCounts[guard])
        if minutesSlept > highest:
            highest = minutesSlept
            chosenGuard = guard

    # find minute slept the most
    count = 0
    chosenMinute = None
    minutes = guardSleepCounts[chosenGuard]
    for i in range(len(minutes)):
        if minutes[i] > count:
            count = minutes[i]
            chosenMinute = i

    print("Part 1 guard ID * minute:", chosenGuard * chosenMinute)


    # PART TWO

    # find most-frequently slept minute and guard
    count = 0
    for guard in guardSleepCounts:
        minutes = guardSleepCounts[guard]

        # look for a minute with higher count
        for i in range(len(minutes)):
            if minutes[i] > count:
                count = minutes[i]
                chosenMinute = i
                chosenGuard = guard

    print("Part 2 guard ID * minute:", chosenGuard * chosenMinute)


if __name__ == "__main__":
    main()
