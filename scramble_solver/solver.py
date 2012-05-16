import pickle
import random
import string
import sys

"""
Solves boggle/scramble with friends
"""

# q doesn't stand by itself since that would not make for a fun game
TOKENS = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','qu','r','s','t','u','v','w','x','y','z']

class Location(object):
  def __init__(self, row, col):
    self.row = row
    self.col = col
    
  def __eq__(self, other):
    return self.row == other.row and self.col == other.col
  
  def __hash__(self):
    return hash((self.row, self.col))  
    
  def __str__(self):
    return '(%d, %d)' %(self.row, self.col)
  
  def __repr__(self):
    return '(%d, %d)' %(self.row, self.col)
  
  def Adjacent(self):
    """Returns the 8 adjacent locations to this one."""
    locs = []
    for row_offset in [-1, 0, 1]:
      for col_offset in [-1, 0, 1]:
        # 0, 0 would be the current location and that's not adjacent
        if not (row_offset == 0 and col_offset == 0):
          locs.append(Location(self.row + row_offset, self.col + col_offset))
    assert len(locs) == 8
    return locs

class FoundWord(object):
  """Represents a discovered word on the board, including the path taken to create it"""

  def __init__(self, word, locations):
    """Initialize object with given string and locations iterable."""
    self.word = word
    self.locations = locations

  def __repr__(self):
    return "%s: %s" %(self.word, self.locations)

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
    """Allow the board to be indexed."""
    return self.board.__getitem__(key)

  def IsValidLocation(self, location):
    row_valid = location.row >= 0 and location.row < self.num_rows
    col_valid = location.col >= 0 and location.col < self.num_cols
    return row_valid and col_valid

class BoardSolver(object):
  def __init__(self, board, dictionary):
    self.board = board
    self.dictionary = dictionary

    self.trie = Trie()
    for index, word in enumerate(dictionary):
      # need 1 based values because 0 is False
      self.trie.add(word, index+1)


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
    for row in range(self.board.num_rows):
      for col in range(self.board.num_cols):
        loc = Location(row, col)
        previous_locs = []
        loc_dict = {}
        solutions.extend(self.DoSolve(previous_locs, loc_dict, loc, ''))

    return solutions

  def DoSolve(self, previous_locations, loc_dict, location, word_prefix):
    """Returns iterable of FoundWord objects.
    
    Args:
      previous_locations: a list of already visited locations
      location: the current Location from where to start searching
      word_prefix: the current word built up so far
    """
    solutions = []

    new_word = word_prefix + self.board[location.row][location.col]
    previous_locations.append(location)
    
    loc_dict_copy = dict(loc_dict)
    loc_dict_copy[location] = True

    # if not self.HasPrefix(new_word):
    #   print 'No words found starting with "%s"' %(new_word)
    #   return solutions
    # 
    # if self.HasWord(new_word):
    #   solutions.append( (new_word, previous_locations) )
    #print previous_locations
    solutions.append( (new_word, previous_locations) )

    # Recursively search all adjacent tiles
    for new_loc in location.Adjacent():
      if self.board.IsValidLocation(new_loc) and new_loc not in loc_dict_copy:
        # make a copy of the previous locations list so it is not affected by this recursive call.
        solutions.extend(self.DoSolve(list(previous_locations), loc_dict_copy, new_loc, new_word))
      else:
        #print 'Illegal move for %s %s %s' %(board_copy, Location(location.row + direction.row_offset, location.col + direction.col_offset), new_word)
        pass

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
  
  output = open("solutions.txt", "wb")
  
  
  # b.board = [
  #     ['A', 'B', 'C'],
  #     ['D', 'E', 'F'],
  #     ['G', 'H', 'I'],    
  #   ]
   
  words = ReadDictionary(sys.argv[1])
  #words = set(['cranes','crates','crash'])
  solver = BoardSolver(b, words)
  #print words
  print b
  solutions = solver.Solve() #set(solver.Solve())
  
  print 'Found %d solutions' %len(solutions)
  pickle.dump(solutions, output)
  # for solution in sorted(solutions):
  #     print solution

  for word, locs in solutions:
    assert len(word) == len(locs), '%s was length %d; only had locs %s' %(word, len(word), locs)
  #assert 'cranes' in solutions
  #assert 'crates' in solutions
  #assert 'crash' in solutions


if __name__ == '__main__':
  main()
