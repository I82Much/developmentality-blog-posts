import random
import string
import sys

"""
Solves boggle/scramble with friends
"""

# q doesn't stand by itself since that would not make for a fun game
TOKENS = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','qu','r','s','t','u','v','w','x','y','z']

class Direction(object):
  def __init__(self, row_offset, col_offset):
    self.row_offset = row_offset
    self.col_offset = col_offset

class Location(object):
  def __init__(self, row, col):
    self.row = row
    self.col = col

DIRECTIONS = [ Direction(delta_row, delta_col) for delta_row in [-1,0,1] for delta_col in [-1,0,1] if delta_row != 0 or delta_col != 0 ]


class FoundWord(object):
  def __init__(self, word, indices):
    self.word = word
    self.indices = indices

  def __repr__(self):
    return "%s: %s" %(self.word, self.indices)

class Board(object):

  def __init__(self):
    # 4x4
    self.board = []
    for i in range(4):
      self.board.append([random.choice(TOKENS) for x in range(4)])

  def __repr__(self):
    return repr(self.board)

  def __str__(self):
    return '\n'.join([str(row) for row in self.board])

  def Solve(self, dictionary):
    """Returns a list of FoundWord objects."""
    solutions = []

    # Start an exhaustive search of the board
    locations = [Location(row, col) for row in range(4) for col in range(4)]
    for location in locations:
      marked_up_board = [
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False]
      ]
      solutions.extend(self.DoSolve(dictionary, marked_up_board, location, ''))

    return solutions

  def IsLegalMove(self, marked_up_board, start_index, direction):
    """Returns true if the new value is within the board and hasn't already been used"""
    new_loc = Location(start_index.row + direction.row_offset, start_index.col + direction.col_offset)
    if new_loc.row >= len(marked_up_board) or new_loc.row < 0:
      return False
    elif new_loc.col >= len(marked_up_board[new_loc.row]) or new_loc.col < 0:
      return False
    # already used
    if marked_up_board[new_loc.row][new_loc.col]:
      return False
    return True

    

  def DoSolve(self, dictionary, marked_up_board, start_index, word_prefix):
    """Returns all possible words."""
    solutions = []

    new_word = word_prefix + self.board[start_index.row][start_index.col]

    found_prefix = False
    for word in dictionary:

      if word.startswith(new_word):
        found_prefix = True
        if word == new_word:
          solutions.append(word)
        continue

    if not found_prefix:
      print 'No words found starting with "%s"' %(new_word)
      return solutions

    # We've used it up
    marked_up_board[start_index.row][start_index.col] = True

    # Recursively search in all directions
    for direction in DIRECTIONS:
      if self.IsLegalMove(marked_up_board, start_index, direction):
        solutions.extend(self.DoSolve(dictionary, marked_up_board, Location(start_index.row + direction.row_offset, start_index.col + direction.col_offset), new_word))
      else:
        print 'Illegal move for %s %s %s' %(marked_up_board, Location(start_index.row + direction.row_offset, start_index.col + direction.col_offset), new_word)

    return solutions


def ReadDictionary(path):
  words = set([])
  f = open(path, "r")
  for line in f:
    words.add(line.lower().strip())
  f.close()
  return words

def main():
  print TOKENS
  #words = set(['red'])

  b = Board()
  b.board = [
    ['n', 'h', 'o', 'l'],
    ['a', 'c', 's', 'r'],
    ['s', 'y', 'a', 'e'],
    ['r', 'p', 'd', 'i']
  ]

  words = ReadDictionary(sys.argv[1])
  #print words
  
  #b = Board()
  print b
  solutions = b.Solve(words)
  
  #words = [ sol.word for sol in solutions ]
  #assert 'red' in solutions #words

  for solution in sorted(solutions):
    print solution
  print 'Found %d solutions' %len(solutions)

if __name__ == '__main__':
  main()
