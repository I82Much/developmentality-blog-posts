from collections import namedtuple

import random
import string
import sys

import trie

"""
Solves Boggle/Scramble with Friends.
"""

TOKENS = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','qu','r','s','t','u','v','w','x','y','z']

DEBUG = False
USE_TRIE = False

class Location(namedtuple('Location', ['row', 'col'])):
  """Represents a location on the board."""
  
  def Adjacent(self):
    """Returns the 8 adjacent locations to this one."""
    locs = []
    for row_offset in [-1, 0, 1]:
      for col_offset in [-1, 0, 1]:
        # 0, 0 would be the current location and that's not adjacent
        if row_offset != 0 or col_offset != 0:
          locs.append(Location(self.row + row_offset, self.col + col_offset))
    assert len(locs) == 8
    return locs

# Represents a discovered word on the board, including the path taken to create it.
FoundWord = namedtuple('FoundWord', ['word', 'locations'])

# TODO(ndunn): Is this board class even necessary
class Board(object):
  """Represents a board, a two dimensional grid of tiles."""
  def __init__(self, num_rows=4, num_cols=4):
    self.num_rows = num_rows
    self.num_cols = num_cols
    self.board = []
    for i in range(num_rows):
      self.board.append([random.choice(TOKENS) for x in range(num_cols)])

  def __repr__(self):
    return repr(self.board)

  def __str__(self):
    return '\n'.join([str(row) for row in self.board])

  def __getitem__(self, key):
    """Allow the board to be indexed."""
    return self.board.__getitem__(key)

  def IsValidLocation(self, location):
    row_valid = location.row >= 0 and location.row < self.num_rows
    col_valid = location.col >= 0 and location.col < self.num_cols
    return row_valid and col_valid

class BoardSolver(object):
  def __init__(self, board, valid_words):
    self.board = board
    self.valid_words = valid_words

    self.trie = trie.Trie()
    for index, word in enumerate(valid_words):
      # 0 evaluates to False which screws up trie lookups; ensure value is 'truthy'.
      self.trie.add(word, index+1)

  def HasPrefix(self, prefix):
    if USE_TRIE:
      return len(self.trie.find_prefix_matches(prefix))
    # Naiive implementation
    else:
      for word in self.valid_words:
        if word.startswith(prefix):
          return True
    return False

  def HasWord(self, word):
    return word in self.valid_words

  def Solve(self):
    """Returns a list of FoundWord objects."""
    solutions = []

    # Start an exhaustive search of the board
    for row in range(self.board.num_rows):
      for col in range(self.board.num_cols):
        loc = Location(row, col)
        previous_locs = []
        solutions.extend(self.DoSolve(previous_locs, loc, ''))

    return solutions

  def DoSolve(self, previous_locations, location, word_prefix):
    """Returns iterable of FoundWord objects.
    
    Args:
      previous_locations: a list of already visited locations
      location: the current Location from where to start searching
      word_prefix: the current word built up so far, as a string
    """
    solutions = []

    new_word = word_prefix + self.board[location.row][location.col]
    previous_locations.append(location)
    
    if not self.HasPrefix(new_word):
      if DEBUG:
        print 'No words found starting with "%s"' %(new_word)
      return solutions
    
    # This is a valid, complete words.
    if self.HasWord(new_word):
      new_solution = FoundWord(new_word, previous_locations)
      if DEBUG:
        print 'Found new solution: %s' %(str(new_solution))
      solutions.append(new_solution)

    # Recursively search all adjacent tiles
    for new_loc in location.Adjacent():
      if self.board.IsValidLocation(new_loc) and new_loc not in previous_locations:
        # make a copy of the previous locations list so our current list
        # is not affected by this recursive call.
        defensive_copy = list(previous_locations)
        solutions.extend(self.DoSolve(defensive_copy, new_loc, new_word))
      else:
        if DEBUG:
          print 'Ignoring %s as it is invalid or already used.' %(new_loc)

    return solutions


def ReadDictionary(path):
  """Returns a set of words found in the file indicated by 'path'."""
  words = set([])
  f = open(path, "r")
  for line in f:
    words.add(line.lower().strip())
  f.close()
  return words


def main():
  b = Board(4, 4)
  # b.board = [['A']]
  # b.board = [
  #   ['u', 'n', 'o', 'l'],
  #   ['e', 't', 'a', 'c'],
  #   ['h', 's', 'r', 'r'],
  #   ['y', 't', 'o', 'h']
  # ]
  # 
  b.board = [
        ['A', 'B', 'C', 'D'],
        ['E', 'F', 'G', 'H'],
        ['I', 'J', 'K', 'L'],
        ['M', 'N', 'O', 'P']
  ]
   
  words = ReadDictionary(sys.argv[1])
  #words = set(['cranes','crates','crash'])
  solver = BoardSolver(b, words)
  #print words
  print b
  solutions = solver.Solve() #set(solver.Solve())
  
  print 'Found %d solutions' %len(solutions)
  # for solution in sorted(solutions):
  #     print solution

  for word, locs in solutions:
    assert len(word) == len(locs), '%s was length %d; only had locs %s' %(word, len(word), locs)
  #assert 'cranes' in solutions
  #assert 'crates' in solutions
  #assert 'crash' in solutions


if __name__ == '__main__':
  main()
