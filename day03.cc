/*
AUTHOR: M. Montgomery 
DATE:   12/03/2018
FILE:   day03.cc 

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

*/

#include <iostream>
#include <string>
#include <vector>
#include <regex>


// Adds a claim to a fabric grid (2D vector), tracking claims per spot
void process(std::vector< std::vector<int> > &fabric,
	     int ID, int x, int y, int width, int height) {

  // add columns as needed
  int cols = x + width;
  while (cols >= fabric.size()) {
    std::vector<int> row(fabric[0].size(), 0);
    fabric.push_back(row);
  }

  // add rows as needed
  int rows = y + height;
  for (int i = 0; i < fabric.size(); i++) {
    while (rows >= fabric[i].size())
      fabric[i].push_back(0);
  }

  // add claim to vector
  for (int i = x; i < x + width; i++) {
    for (int j = y; j < y + height; j++)
      fabric[i][j] += 1;
  }
}


// Tallies the overlapping square inches given a fabric grid
int overlappingArea(std::vector< std::vector<int> > &fabric) {

  int total = 0;
  for (int i = 0; i < fabric.size(); i++) {
    for (int j = 0; j < fabric[i].size(); j++) {
      if (fabric[i][j] > 1)
	total += 1;
    }
  }
  return total;
}


int main() {

  // initialize 1000x1000 grid (minimum size)
  std::vector< std::vector<int> > fabric;
  for (int i = 0; i < 1000; i++) {
    std::vector<int> row(1000, 0);
    fabric.push_back(row);
  }

  // define regex for claim format:
  // #[ID] @ [x],[y]: [width]x[height]
  const std::regex claim("^#(\\d+) @ (\\d+),(\\d+): (\\d+)x(\\d+)$");
  std::smatch matches;

  // read and process claims
  std::string line;
  int ID, x, y, width, height;
  while (getline(std::cin, line)) {

    // map line to claim format
    if (regex_search(line, matches, claim)) {

      // extract values
      ID     = std::stoi(matches[1]);
      x      = std::stoi(matches[2]);
      y      = std::stoi(matches[3]);
      width  = std::stoi(matches[4]);
      height = std::stoi(matches[5]);

      // process the claim
      process(fabric, ID, x, y, width, height);
    }
  }

  // PART ONE
  std::cout << "There are " << overlappingArea(fabric) <<
    " square inches of fabric with one or more claims." << std::endl;
  
  return 0;
}
