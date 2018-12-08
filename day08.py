"""
AUTHOR: M. Montgomery 
DATE:   12/08/2018
FILE:   day08.py 

PROMPT: 
--- Day 8: Memory Maneuver ---

The sleigh is much easier to pull than you'd expect for something its weight. Unfortunately, neither you nor the Elves know which way the North Pole is from here. You check your wrist device for anything that might help. It seems to have some kind of navigation system! Activating the navigation system produces more bad news: "Failed to start navigation system. Could not read software license file."

The navigation system's license file consists of a list of numbers (your puzzle input). The numbers define a data structure which, when processed, produces some kind of tree that can be used to calculate the license number. The tree is made up of nodes; a single, outermost node forms the tree's root, and it contains all other nodes in the tree (or contains nodes that contain nodes, and so on).

Specifically, a node consists of: A header, which is always exactly two numbers (the quantity of child nodes; the quantity of metadata entries); Zero or more child nodes (as specified in the header); One or more metadata entries (as specified in the header). Each child node is itself a node that has its own header, child nodes, and metadata. For example:

2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
A----------------------------------
    B----------- C-----------
                     D-----

In this example, each node of the tree is also marked with an underline starting with a letter for easier identification. In it, there are four nodes:

    A, which has 2 child nodes (B, C) and 3 metadata entries (1, 1, 2).
    B, which has 0 child nodes and 3 metadata entries (10, 11, 12).
    C, which has 1 child node (D) and 1 metadata entry (2).
    D, which has 0 child nodes and 1 metadata entry (99).

The first check done on the license file is to simply add up all of the metadata entries. In this example, that sum is 1+1+2+10+11+12+2+99=138.

What is the sum of all metadata entries?

--- Part Two ---

The second check is slightly more complicated: you need to find the value of the root node (A in the example above).

The value of a node depends on whether it has child nodes.

If a node has no child nodes, its value is the sum of its metadata entries. So, the value of node B is 10+11+12=33, and the value of node D is 99.

However, if a node does have child nodes, the metadata entries become indexes which refer to those child nodes. A metadata entry of 1 refers to the first child node, 2 to the second, 3 to the third, and so on. The value of this node is the sum of the values of the child nodes referenced by the metadata entries. If a referenced child node does not exist, that reference is skipped. A child node can be referenced multiple time and counts each time it is referenced. A metadata entry of 0 does not refer to any child node.

For example, again using the above nodes:

Node C has one metadata entry, 2. Because node C has only one child node, 2 references a child node which does not exist, and so the value of node C is 0. Node A has three metadata entries: 1, 1, and 2. The 1 references node A's first child node, B, and the 2 references node A's second child node, C. Because node B has a value of 33 and node C has a value of 0, the value of node A is 33+33+0=66. So, in this example, the value of the root node is 66.

What is the value of the root node?
"""

import sys

class Node:
    def __init__(self, numChildren, numMetadata):
        self.numChildren = numChildren
        self.numMetadata = numMetadata
        self.children = []
        self.metadata = []

    def addChild(self, node):
        self.children.append(node)

    def addMetadata(self, data):
        self.metadata.append(data)

    def getMetadata(self):
        return self.metadata

    def getChildren(self):
        return self.children

    def __str__(self):
        return str(self.numChildren) +  " children; " +\
            str(self.numMetadata) + " metadata"    

    
def buildTree(numbers, index=0):
    """ Given a list of numbers and a starting index, returns a node
        and the new starting index after reading in the node's data
        (including recursing for children). """
    
    # build node at given index
    numChildren = numbers[index]
    numMetadata = numbers[index+1]
    current = Node(numChildren, numMetadata)

    # recurse to build children
    index += 2
    for _ in range(numChildren):
        child, index = buildTree(numbers, index)
        current.addChild(child)

    # add metadata
    for i in range(numMetadata):
        current.addMetadata(numbers[index+i])

    return current, index + numMetadata


def getMetadataSum(current):
    """ Given a node, returns sum of node's metadata plus the sum of all 
        the node's childrens' metadata. """

    return sum(current.getMetadata()) +\
        sum([getMetadataSum(child) for child in current.getChildren()])


def getNodeValue(node):
    """ Given a node, returns its value. """

    # value is metadata sum if no children
    children = node.getChildren()
    if len(children) == 0:
        return sum(node.getMetadata())

    # value is sum of childrens' values
    value = 0
    for i in node.getMetadata():         # i=1 means 1st child, etc.
        if i > 0 and i <= len(children):
            value += getNodeValue(children[i-1])

    return value


def main():

    # get input
    numbers = [int(n) for n in sys.stdin.readline().strip().split(" ")]
    tree, _ = buildTree(numbers)

    # PART ONE
    metadataSum = getMetadataSum(tree)
    print("Metadata sum:", metadataSum)

    # PART TWO
    rootValue = getNodeValue(tree)
    print("Root value:", rootValue)
    
    
if __name__ == "__main__":
    main()
