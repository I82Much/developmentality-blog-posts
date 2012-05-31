import random

# q doesn't stand by itself since that would not make for a fun game
TOKENS = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','qu','r','s','t','u','v','w','x','y','z']

class Direction(object):
  def __init__(self, row_offset, col_offset):
    self.row_offset = row_offset
    self.col_offset = col_offset

DIRECTIONS = [ Direction(delta_row, delta_col) for delta_row in [-1,0,1] for delta_col in [-1,0,1] if delta_row != 0 or delta_col != 0 ]
assert len(DIRECTIONS) == 8

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

  def AdjacentLocations(self):
    return [Location(self.row + dir.row_offset, self.col + dir.col_offset) for dir in DIRECTIONS]


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
    
  def ValidLocation(self, loc):
    valid_row = loc.row >= 0 and loc.row < self.num_rows
    valid_col = loc.col >= 0 and loc.col < self.num_cols
    return valid_row and valid_col
  
  def ElemAtLocation(self, loc):
    assert self.ValidLocation(loc)
    return self.board[loc.row][loc.col]


def DFS(board, start_loc):
  stack = []
  visited = {}
  predecessors = {}

  for row in range(board.num_rows):
    for col in range(board.num_cols):
      visited[Location(row, col)] = False
  stack.append(start_loc)
  while len(stack) > 0:
    print stack
    loc = stack.pop()
    if not visited[loc]:
      visited[loc] = True
      for adj_loc in loc.AdjacentLocations():
        if board.ValidLocation(adj_loc) and not visited[adj_loc]:
          stack.append(adj_loc)

def main():
  # board = [
  #     ['A', 'B', 'C', 'D'],
  #     ['E', 'F', 'G', 'H'],
  #     ['I', 'J', 'K', 'L'],
  #     ['M', 'N', 'O', 'P']
  #   ]
  
  # depth first search
  
  board = [
    ['A', 'B'],
    ['C', 'D']
  ]
  b = Board(2, 2)
  b.board = board

  DFS(b, Location(0,0))

  # while len(stack) > 0:# and iters < 20:
  #     print 'Stack:\t%s\tCurrent Path%s' %(map(l_to_tile, stack), map(l_to_tile, path))
  #     
  #     cur_loc = stack.pop()
  #     if cur_loc in path:
  #       print 'Ignoring %s' %(l_to_tile(cur_loc))
  #       continue
  #       
  #     path.append(cur_loc)
  #     
  #     paths.append(list(path))
  #     
  #     bad_locs = []
  #     for loc in cur_loc.AdjacentLocations():
  #       if b.ValidLocation(loc):
  #         stack.append(loc)
  #             # 
  #             # if loc in path or not b.ValidLocation(loc):
  #             #   bad_locs.append(loc)
  #             # 
  #             # # It's ok
  #             # else:
  #             #   print 'Adding ' + l_to_tile(loc)
  #             #   stack.append(loc)
  # 
  #     # All are bad - backtrack
  #     # if len(bad_locs) == len(cur_loc.AdjacentLocations()):
  #     #       print 'Nowhere left to go from path %s' %map(l_to_tile, path)
  #     #       path.pop()
  #     #         
  #     #     iters += 1
    
  # print map(lambda list: map(l_to_tile, list), paths)  

if __name__ == '__main__':
  main()