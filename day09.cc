/*
AUTHOR: M. Montgomery 
DATE:   12/09/2018
FILE:   day09.cc 

PROMPT: 
*/

#include <iostream>
#include <vector>
#include <regex>

size_t getScore(int NPlayers, int NMarbles) {

  size_t scores[NPlayers] = {0};
  std::vector<size_t> marbles = {0,1};
  std::vector<size_t>::iterator current = marbles.begin() + 1;
  std::vector<size_t>::iterator other;

  for (size_t marble = 2; marble <= NMarbles; marble++) {

    // special case for multiples of 23
    if (marble % 23 == 0) {

      // add marble to score
      size_t currentPlayer = marble % NPlayers;
      scores[currentPlayer] += marble;

      // find marble 7 away (counterclockwise)
      int i;
      for (other = current, i = 0;
	   other != marbles.begin() && i < 7;
	   other--, i++);
      if (other == marbles.begin() && i < 7)
	other = marbles.end() - (7 - i);

      // remove marble and add to score
      scores[currentPlayer] += *other;
      current = marbles.erase(other);
    }

    // insert marble 2 places away (clockwise)
    else {

      if (current+1 == marbles.end())
	other = marbles.begin() + 1;
      else if (current+2 == marbles.end())
	other = marbles.end();
      else
	other = current + 2;

      current = marbles.insert(other, marble);
    }
  }

  // return highest score
  size_t highest = 0;
  for (int i = 0; i < NPlayers; i++) {
    if (scores[i] > highest)
      highest = scores[i];
  }
  return highest;
}


int main() {
  
  const std::regex Rline("(\\d+) players; last marble is worth (\\d+) points");
  std::smatch matches;
  std::string line;
  size_t NPlayers, NMarbles;
  
  while (getline(std::cin, line)) {

    // map line to regex format
    if (regex_search(line, matches, Rline)) {

      // extract values
      NPlayers = std::stoi(matches[1]);
      NMarbles = std::stoi(matches[2]);

      // PART ONE
      size_t score = getScore(NPlayers, NMarbles);
      std::cout << line << ": high score: " << score << std::endl;

      // PART TWO
      score = getScore(NPlayers, NMarbles * 100);
      std::cout << "New high score: " << score << std::endl;
    }
  }
  
  return 0;
}
