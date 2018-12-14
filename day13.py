"""
AUTHOR: M. Montgomery 
DATE:   12/13/2018
FILE:   day13.py 

PROMPT: 
--- Day 13: Mine Cart Madness ---

A crop of this size requires significant logistics to transport produce, soil, fertilizer, and so on. The Elves are very busy pushing things around in carts on some kind of rudimentary system of tracks they've come up with. Seeing as how cart-and-track systems don't appear in recorded history for another 1000 years, the Elves seem to be making this up as they go along. They haven't even figured out how to avoid collisions yet. You map out the tracks (your puzzle input) and see where you can help.

Tracks consist of straight paths (| and -), curves (/ and \), and intersections (+). Curves connect exactly two perpendicular pieces of track; for example, this is a closed loop:

/----\
|    |
|    |
\----/

Intersections occur when two perpendicular paths cross. At an intersection, a cart is capable of turning left, turning right, or continuing straight. Here are two loops connected by two intersections:

/-----\
|     |
|  /--+--\
|  |  |  |
\--+--/  |
   |     |
   \-----/

Several carts are also on the tracks. Carts always face either up (^), down (v), left (<), or right (>). (On your initial map, the track under each cart is a straight path matching the direction the cart is facing.)

Each time a cart has the option to turn (by arriving at any intersection), it turns left the first time, goes straight the second time, turns right the third time, and then repeats those directions starting again with left the fourth time, straight the fifth time, and so on. This process is independent of the particular intersection at which the cart has arrived - that is, the cart has no per-intersection memory.

Carts all move at the same speed; they take turns moving a single step at a time. They do this based on their current location: carts on the top row move first (acting from left to right), then carts on the second row move (again from left to right), then carts on the third row, and so on. Once each cart has moved one step, the process repeats; each of these loops is called a tick.

For example, suppose there are two carts on a straight track:

|  |  |  |  |
v  |  |  |  |
|  v  v  |  |
|  |  |  v  X
|  |  ^  ^  |
^  ^  |  |  |
|  |  |  |  |

First, the top cart moves. It is facing down (v), so it moves down one square. Second, the bottom cart moves. It is facing up (^), so it moves up one square. Because all carts have moved, the first tick ends. Then, the process repeats, starting with the first cart. The first cart moves down, then the second cart moves up - right into the first cart, colliding with it! (The location of the crash is marked with an X.) This ends the second and last tick.

Here is a longer example:

/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   

/-->\        
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \->--/
  \------/   

/---v        
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+>-/
  \------/   

/---\        
|   v  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+->/
  \------/   

/---\        
|   |  /----\
| /->--+-\  |
| | |  | |  |
\-+-/  \-+--^
  \------/   

/---\        
|   |  /----\
| /-+>-+-\  |
| | |  | |  ^
\-+-/  \-+--/
  \------/   

/---\        
|   |  /----\
| /-+->+-\  ^
| | |  | |  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /----<
| /-+-->-\  |
| | |  | |  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /---<\
| /-+--+>\  |
| | |  | |  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /--<-\
| /-+--+-v  |
| | |  | |  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /-<--\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /<---\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-<--/
  \------/   

/---\        
|   |  v----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \<+--/
  \------/   

/---\        
|   |  /----\
| /-+--v-\  |
| | |  | |  |
\-+-/  ^-+--/
  \------/   

/---\        
|   |  /----\
| /-+--+-\  |
| | |  X |  |
\-+-/  \-+--/
  \------/   

After following their respective paths for a while, the carts eventually crash. To help prevent crashes, you'd like to know the location of the first crash. Locations are given in X,Y coordinates, where the furthest left column is X=0 and the furthest top row is Y=0:

           111
 0123456789012
0/---\        
1|   |  /----\
2| /-+--+-\  |
3| | |  X |  |
4\-+-/  \-+--/
5  \------/   

In this example, the location of the first crash is 7,3.
--- Part Two ---

There isn't much you can do to prevent crashes in this ridiculous system. However, by predicting the crashes, the Elves know where to be in advance and instantly remove the two crashing carts the moment any crash occurs.

They can proceed like this for a while, but eventually, they're going to run out of carts. It could be useful to figure out where the last cart that hasn't crashed will end up.

For example:

/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/

/---\  
|   |  
| v-+-\
| | | |
\-+-/ |
  |   |
  ^---^

/---\  
|   |  
| /-+-\
| v | |
\-+-/ |
  ^   ^
  \---/

/---\  
|   |  
| /-+-\
| | | |
\-+-/ ^
  |   |
  \---/

After four very expensive crashes, a tick ends with only one cart remaining; its final location is 6,4.

What is the location of the last cart at the end of the first tick where it is the only cart left?
"""

import sys

UP    = 0
RIGHT = 1
DOWN  = 2
LEFT  = 3

DIRS   = { "^": UP, ">": RIGHT, "v": DOWN, "<": LEFT }
CHARS  = { UP: "^", RIGHT: ">", DOWN: "v", LEFT: "<" }
DELTAS = [[ 0,-1], [ 1, 0], [ 0, 1], [-1, 0]]

EMPTY = " "

class Cart:

    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.delta = DIRS[char]
        self.turn = 0
        
    def coords(self):
        return (self.x, self.y)

    def intersect(self):
        # first time: turn left
        if self.turn == 0:
            self.delta -= 1

        # third time: turn right
        elif self.turn == 2:
            self.delta += 1

        # cycle turn status
        self.turn = (self.turn + 1) % 3

    def move(self, track):

        # intersection
        if track == "+":
            self.intersect()
        
        # curve
        elif track == "/":
            self.delta += 1 if self.delta in [UP, DOWN] else -1
            
        elif track == "\\":
            self.delta += 1 if self.delta in [RIGHT, LEFT] else -1

        # update coordinates
        self.delta %= 4
        self.x += DELTAS[self.delta][0]
        self.y += DELTAS[self.delta][1]


def findCollision(tracks, carts):

    # continue until collision
    while True:

        # queue up carts for moving
        carts = sorted(carts, key=lambda cart:(cart.x, cart.y))

        # move each cart in order
        for cart in carts:
        
            # move and check for collision
            x,y = cart.coords()
            cart.move(tracks[y][x])
            x,y = cart.coords()

            # remove crashed carts
            if (x,y) in [(other.x,other.y) for other in carts if other != cart]:
                return x,y
                
        
def findLastCart(tracks, carts):

    # continue until 1 cart left
    while len(carts) > 1:

        # queue up carts for moving
        carts = sorted(carts, key=lambda cart:(cart.x, cart.y))

        # move each cart in order
        for cart in carts:
        
            # move and check for collision
            x,y = cart.coords()
            cart.move(tracks[y][x])
            x,y = cart.coords()

            # remove crashed carts
            if (x,y) in [(other.x,other.y) for other in carts if other != cart]:
                carts = [other for other in carts if \
                         (other.x,other.y) not in [(x,y)]]
        
    # return last cart's coordinates
    return carts[0].x, carts[0].y


def main():

    # get input
    lines = [line.rstrip() for line in sys.stdin.readlines()]
    width = max([len(line) for line in lines])
    tracks = [[EMPTY] * width for _ in range(len(lines))]
    
    # replace carts with tracks beneath them
    straight = {
        ">" : "-", "<" : "-",
        "^" : "|", "v" : "|"
    }
    
    # add tracks, carts to grid
    carts1 = []
    carts2 = []
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            char = lines[y][x]

            # handle a cart
            if char in "<>^v":
                tracks[y][x] = straight[char]
                carts1.append(Cart(x, y, char))
                carts2.append(Cart(x, y, char))
            else:
                tracks[y][x] = char

    # PART ONE
    collision = findCollision(tracks, carts1)
    print("First collision:", collision)

    # PART TWO
    coords = findLastCart(tracks, carts2)
    print("Last cart is at:", coords)

    
if __name__ == "__main__":
    main()
