import abc
from abc import ABCMeta
from collections import namedtuple


import pickle

import bisect
import random
import string
import sys

import trie

"""
Solves Boggle/Scramble with Friends.
"""

TOKENS = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','qu','r','s','t','u','v','w','x','y','z']

DEBUG = False
PREFIX_PRUNE = False

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
  __metaclass__ = ABCMeta

  @abc.abstractmethod
  def HasPrefix(self, prefix):
    pass

  @abc.abstractmethod
  def HasWord(self, prefix):
    pass

  def Solve(self, board):
    """Returns a list of FoundWord objects."""
    solutions = []

    # Start an exhaustive search of the board
    for row in range(board.num_rows):
      for col in range(board.num_cols):
        loc = Location(row, col)
        previous_locs = []
        solutions.extend(self.DoSolve(board, previous_locs, loc, ''))

    return solutions

  def DoSolve(self, board, previous_locations, location, word_prefix):
    """Returns iterable of FoundWord objects.

    Args:
      previous_locations: a list of already visited locations
      location: the current Location from where to start searching
      word_prefix: the current word built up so far, as a string
    """
    solutions = []

    new_word = word_prefix + board[location.row][location.col]
    previous_locations.append(location)

    if PREFIX_PRUNE and not self.HasPrefix(new_word):
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
      if board.IsValidLocation(new_loc) and new_loc not in previous_locations:
        # make a copy of the previous locations list so our current list
        # is not affected by this recursive call.
        defensive_copy = list(previous_locations)
        solutions.extend(self.DoSolve(board, defensive_copy, new_loc, new_word))
      else:
        if DEBUG:
          print 'Ignoring %s as it is invalid or already used.' %(str(new_loc))

    return solutions


class UnsortedListBoardSolver(BoardSolver):
  def __init__(self, valid_words):
    self.valid_words = valid_words

  def HasPrefix(self, prefix):
    for word in self.valid_words:
      if word.startswith(prefix):
        return True
    return False

  def HasWord(self, word):
    return word in self.valid_words

class SetBoardSolver(BoardSolver):
  def __init__(self, valid_words):
    self.valid_words = set(valid_words)

  def HasPrefix(self, prefix):
    for word in self.valid_words:
      if word.startswith(prefix):
        return True
    return False

  def HasWord(self, word):
    return word in self.valid_words

class DictBoardSolver(BoardSolver):
  def __init__(self, valid_words):
    self.valid_words = dict([(word, True) for word in valid_words])

  def HasPrefix(self, prefix):
    for word in self.valid_words:
      if word.startswith(prefix):
        return True
    return False

  def HasWord(self, word):
    return word in self.valid_words

class SortedListBoardSolver(BoardSolver):
  def __init__(self, valid_words):
    self.valid_words = sorted(valid_words)

  # http://docs.python.org/library/bisect.html#searching-sorted-lists
  def index(self, a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
      return i
    raise ValueError
  
  def find_ge(self, a, x):
    'Find leftmost item greater than or equal to x'
    i = bisect.bisect_left(a, x)
    if i != len(a):
      return a[i]
    raise ValueError  

  def HasPrefix(self, prefix):
    try:
      word = self.find_ge(self.valid_words, prefix)
      return word.startswith(prefix)
    except ValueError:
      return False
    
  def HasWord(self, word):
    try:
      self.index(self.valid_words, word)
    except ValueError:
      return False
    return True
  

class TrieBoardSolver(BoardSolver):
  def __init__(self, valid_words):
    self.trie = trie.Trie()
    for index, word in enumerate(valid_words):
      # 0 evaluates to False which screws up trie lookups; ensure value is 'truthy'.
      self.trie.add(word, index+1)
  
  def HasPrefix(self, prefix):
    curr_node, remainder = self.trie._find_prefix_match(prefix)
    return not remainder
    # Bug
    #   return len(self.trie.find_prefix_matches(prefix)) > 0

  def HasWord(self, word):
    return word in self.trie
  
def ReadDictionary(path):
  """Returns a set of words found in the file indicated by 'path'."""
  words = set([])
  f = open(path, "r")
  for line in f:
    words.add(line.lower().strip())
  f.close()
  return words


def main():
  
  # Unsorted lists
  
  # http://docs.python.org/library/bisect.html
  # Sorted list with bisect
  
  
  words = ReadDictionary(sys.argv[1])
  trie_solver = TrieBoardSolver(words)
  list_solver = UnsortedListBoardSolver(words)
  set_solver = SetBoardSolver(words)
  dict_solver = DictBoardSolver(words)
  sorted_list_solver = SortedListBoardSolver(words)
  
  # print 'Size of trie solver pickled: %d' %(len(pickle.dumps(trie_solver, -1)))
  #   print 'Size of list solver pickled: %d' %(len(pickle.dumps(list_solver, -1)))
  #   print 'Size of sorted list solver pickled: %d' %(len(pickle.dumps(sorted_list_solver, -1)))


  import datetime
  
  
  iters = [1]#, 100] #, 1000, 10000, 100000]
  #solvers = [list_solver,set_solver, dict_solver, trie_solver, sorted_list_solver]
  
  solvers = [set_solver, dict_solver]
  for num_iters in iters:
    random_boards = [Board(4,4) for x in range(num_iters)]
    for solver in solvers:
      start = datetime.datetime.now()
      for board in random_boards:
        solver.Solve(board)
      end = datetime.datetime.now()
      elapsed = end - start
    
      seconds = elapsed.seconds + (elapsed.microseconds / 1E6)
      avg_time = seconds / num_iters
      print 'Took %.3f seconds to solve %d boards; avg %.3f with %s' %(elapsed.seconds, 
        num_iters, avg_time, solver)
  
  # Took 23.00 seconds to solve 10 boards; avg 2.36 with <__main__.TrieBoardSolver object at 0x198c770>
  #   Took 0.00 seconds to solve 10 boards; avg 0.03 with <__main__.SortedListBoardSolver object at 0x198c870>
  
  #$ wc -l /usr/share/dict/words
  #  234936 /usr/share/dict/words
  # >>> import math
  #   >>> math.log(234936) / math.log(2)   
  #   17.841908273534177
  #   >>> 2**18
  #   262144
  
  
  # b = Board(4, 4)
  #   # b.board = [
  #   #          ['h', 'b', 'c', 'd'],
  #   #          ['e', 'f', 'G', 'h'],
  #   #          ['i', 'l', 'l', 'l'],
  #   #          ['m', 'n', 'o', 'p']
  #   #   ]
  #   
  #   b.board = [
  #          ['i', 'd', 'w', 'c'],
  #          ['s', 'n', 'a', 'k'],
  #          ['t', 'u', 'p', 'e'],
  #          ['d', 's', 'g', 'e']
  #   ]
  #   
  #   print b
  #   solutions = sorted_list_solver.Solve(b)
  #  
  #print 'Found %d solutions' %len(solutions)
  #print 'Found %d solutions' %len(list_solver.Solve(b))
  #print 'Found %d solutions' %len(trie_solver.Solve(b))
    
  # for solution in sorted(solutions):
  #      print solution
  # 
  #   for word, locs in solutions:
  #     # Every tile takes up one letter, except qu
  #     expected_len = len(locs) - word.count('q')
  #     assert len(word) == expected_len, '%s was length %d; only had %d tiles' %(
  #       word, len(word), len(locs))
  

if __name__ == '__main__':
  main()
