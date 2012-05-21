# From https://bitbucket.org/woadwarrior/trie/src/6bc187d770ba/python/trie.py


_SENTINEL = ()

class Trie(object) :
  __slots__ = ['root']

  def __init__( self ) :
      # what does the dict map from
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
      # Traverse through the nodes
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
      # If there's a remainder, then there's nothing in the tree that matches
      if l[1] :
          return []
      # stack starts ith the current node
      stack = [l[0]]
      ret = []
      while stack :
          d = stack.pop()
          if d[0] :
              ret.insert(0,d[0])
          for c in d[1] :
              stack.append(d[1][c])
      return ret
