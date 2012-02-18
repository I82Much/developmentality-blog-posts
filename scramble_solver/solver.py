import random
import string
import sys

"""
Solves boggle/scramble with friends
"""

# q doesn't stand by itself since that would not make for a fun game
TOKENS = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','qu','r','s','t','u','v','w','x','y','z']


class Board(object):

  def __init__(self):
    # 4x4
    self.board = []
    for row in range(4):
      row = []
      for col in range(4):
        self.board[row][col] = random.choice(TOKENS)

  def __repr__(self):
    return repr(self.board)

  

def ReadDictionary(path):
  words = set([])
  f = open(path, "r")
  for line in f:
    words.add(line.lower().strip())
  f.close()
  return words

def main():
  print TOKENS
  words = ReadDictionary(sys.argv[1])
  print words
  
  b = Board()
  print b

if __name__ == '__main__':
  main()