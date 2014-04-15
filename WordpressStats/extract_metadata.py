import collections
import re

post_id_re = re.compile('<tr id="post-([^"]*)"')
category_id_re = re.compile('.*category-([^ ]*)')
tag_re = re.compile('.*tag-([^ ]*)')

title_re = re.compile('.*>([^<]*)</a>')
post_id_re_from_title = re.compile('.*post=([0-9]*)')

post_metadata = collections.namedtuple('metadata', ['id', 'title', 'categories', 'tags'])

def main():
  a = """href="https://developmentality.wordpress.com/wp-admin/post.php?post=357234106&amp;action=edit"""
  print post_id_re_from_title.match(a)
  
  posts = {}
  
  for line in open("all_posts.html"):
    line = line.strip()
    
    # Most metadata comes from this line. e.g.
    # <tr id="post-369875749" class="post-369875749 type-post status-publish format-standard hentry category-uncategorized tag-exception tag-netbeans tag-workaround alternate iedit author-self level-0" valign="top">
    if '<tr id=' in line:
      post_id = post_id_re.match(line).group(1)
    
      m = category_id_re.match(line)
      categories = []
      if m:
        categories = m.groups()
    
      tags = []
      c = tag_re.match(line)
      if c:
        tags = c.groups()
      
      p = post_metadata(id=post_id, title='', categories=categories, tags=tags)
      posts[p.id] = p
    
    elif '<td class="post-title page-title column-title">' in line:
      post_id_match = post_id_re_from_title.match(line)
      #if not post_id_match:
        #print line
      post_id = post_id_match.group(1)
      
      title_match = title_re.match(line)
      if title_match:
        p = posts[post_id]
        p2 = post_metadata(id=p.id, title=title_match.group(1), categories=p.categories, tags=p.tags)
        posts[post_id] = p2
        
  for k, p in sorted(posts.items()):
    print p
      
    

if __name__ == '__main__':
	main()