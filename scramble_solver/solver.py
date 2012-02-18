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
    return self.board.__getitem__(key)

class BoardSolver(object):
  def __init__(self, board, dictionary):
    self.board = board
    self.dictionary = dictionary


    self.trie = Trie()
    for index, word in enumerate(dictionary):
      self.trie.add(word, index)


  def HasPrefix(self, prefix):
    return len(self.trie.find_prefix_matches(prefix))
    # Naiive implementation
    #for word in self.dictionary:
    #  if word.startswith(prefix):
    #    return True
    #return False

  def HasWord(self, word):
    return word in self.dictionary

  def Solve(self):
    """Returns a list of FoundWord objects."""
    solutions = []

    # Start an exhaustive search of the board
    locations = [Location(row, col) for row in range(self.board.num_rows) for col in range(self.board.num_cols)]
    for location in locations:
      marked_up_board = []
      for row in range(self.board.num_rows):
        marked_up_board.append( [False] * self.board.num_cols)
      solutions.extend(self.DoSolve(marked_up_board, location, ''))

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

  def DoSolve(self, marked_up_board, start_index, word_prefix):
    """Returns all possible words."""
    solutions = []

    new_word = word_prefix + self.board[start_index.row][start_index.col]

    if not self.HasPrefix(new_word):
      print 'No words found starting with "%s"' %(new_word)
      return solutions

    if self.HasWord(new_word):
      solutions.append(new_word)
     
    # We've used it up
    marked_up_board[start_index.row][start_index.col] = True

    # Recursively search in all directions
    for direction in DIRECTIONS:
      if self.IsLegalMove(marked_up_board, start_index, direction):
        solutions.extend(self.DoSolve(marked_up_board, Location(start_index.row + direction.row_offset, start_index.col + direction.col_offset), new_word))
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

# From https://bitbucket.org/woadwarrior/trie/src/6bc187d770ba/python/trie.py
_SENTINEL = ()

class Trie(object) :
    __slots__ = ['root']

    def __init__( self ) :
        self.root = [None,{}]

    def __getstate__( self ) :
        if any(self.root) :
            return self.root
        else :
            return False

    def __setstate__(self, s) :
        self.root = s

    def __contains__( self, s ) :
        if self.find_full_match(s,_SENTINEL) is _SENTINEL :
            return False
        return True

    def add( self, key, value ) :
        curr_node = self.root
        for ch in key :
            node = curr_node[1]
            if ch in node :
                curr_node = node[ch]
            else :
                curr_node = node[ch] = [None,{}]
        curr_node[0] = value

    def _find_prefix_match( self, key ) :
        curr_node = self.root
        remainder = key
        for ch in key :
            if ch in curr_node[1] :
                curr_node = curr_node[1][ch]
            else :
                break
            remainder = remainder[1:]
        return [curr_node,remainder]

    def find_full_match( self, key, fallback=None ) :
        '''
        Returns the value associated with the key if found else, returns fallback
        '''
        r = self._find_prefix_match( key )
        if not r[1] and r[0] :
            return r[0][0]
        return fallback

    def find_prefix_matches( self, prefix ) :
        l = self._find_prefix_match( prefix )
        if l[1] :
            return []
        stack = [l[0]]
        ret = []
        while stack :
            d = stack.pop()
            if d[0] :
                ret.insert(0,d[0])
            for c in d[1] :
                stack.append(d[1][c])
        return ret

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

  b.board = [
    ['u', 'n', 'o', 'l'],
    ['e', 't', 'a', 'c'],
    ['h', 's', 'r', 'r'],
    ['y', 't', 'o', 'h']
  ]



  words = ReadDictionary(sys.argv[1])
  solver = BoardSolver(b, words)
  #print words
  
  #b = Board()
  print b
  solutions = solver.Solve()
  
  #words = [ sol.word for sol in solutions ]
  #assert 'red' in solutions #words

  for solution in sorted(solutions):
    print solution
  print 'Found %d solutions' %len(solutions)

if __name__ == '__main__':
  main()
