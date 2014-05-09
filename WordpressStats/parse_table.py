# This script parses the HTML table that contains the Published data for your Wordpress.com blog.
# https://developmentality.wordpress.com/wp-admin/edit.php?post_status=publish&post_type=post&orderby=title&order=asc

import collections
import csv
import codecs
import cStringIO
import sys
from bs4 import BeautifulSoup

columns = ['id', 'publish_date', 'title', 'link', 'categories', 'tags']
post_metadata = collections.namedtuple('metadata', columns)


# from http://docs.python.org/2/library/csv.html#csv.writer
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def main():
  soup = BeautifulSoup(open("all_posts.html"))
  # Extract all of the tr id="post" rows.
  # <tr id="post-357234106" class="post-357234106 type-post status-publish format-standard hentry category-photo alternate iedit author-self level-0" valign="top">
  trs = soup.find_all('tr')
  posts = []
  for tr in trs:
    post_id = tr.get('id')
    # Only care about the tr's with ids. These represent the posts.
    if post_id is None:
      continue
    # Get the post ID
    # id="post-xyz" -> "xyz"  
    post_id = post_id.replace('post-', '')
    
    # Get the published URL
    url = tr.find('a', text='View')['href']

    # Lots of metadata is hidden:
    # Tags
    # <div class="hidden" id="inline_369875742">
    #   <div class="post_title">Args4j library for parsing Java command line arguments</div>
    #   <div class="post_name">args4j-library-for-parsing-java-command-line-arguments</div>
    #   <div class="post_author">881869</div>
    #   <div class="comment_status">open</div>
    #   <div class="ping_status">open</div>
    #   <div class="_status">publish</div>
    #   <div class="jj">11</div>
    #   <div class="mm">05</div>
    #   <div class="aa">2010</div>
    #   <div class="hh">21</div>
    #   <div class="mn">44</div>
    #   <div class="ss">58</div>
    #   <div class="post_password"></div><div class="post_category" id="category_369875742">355753,1</div><div class="tags_input" id="post_tag_369875742">args4j, command line, java, parsing</div><div class="sticky"></div><div class="post_format"></div></div>
   
    # Pull out the title, publish date
    metadata = tr.find('div', class_='hidden')
    title = metadata.find('div', class_='post_title').text
    publish_day = metadata.find('div', class_='jj').text
    publish_month = metadata.find('div', class_='mm').text
    publish_year = metadata.find('div', class_='aa').text
    publish_date = '%s-%s-%s' %(publish_year, publish_month, publish_day)
    
    # Find the tags
    tags = []
    tags_div = metadata.find('div', class_='tags_input')
    if tags_div:
      tags = tags_div.text.split(', ')
      #tags = [x.encode('ascii', 'ignore') for x in tags]
    
    # Find the categories
    categories_td = tr.find('td', class_='column-categories')
    #categories = [x.text.encode('ascii', 'ignore') for x in categories_td.find_all('a')]
    categories = [x.text for x in categories_td.find_all('a')]
    
    data = post_metadata(id=post_id.encode('ascii', 'ignore'),
                    publish_date=publish_date.encode('ascii', 'ignore'),
                    title=title.encode('ascii', 'ignore'),
                    link=url.encode('ascii', 'ignore'),
                    categories=categories,
                    tags=tags)
                    
    data = post_metadata(id=post_id,
                    publish_date=publish_date,
                    title=title,
                    link=url,
                    categories=categories,
                    tags=tags)                

    posts.append(data)

  # Cannot use standard csv writer because of the unicode in the table.
  # See http://stackoverflow.com/questions/1846135/python-csv-library-with-unicode-utf-8-support-that-just-works
  # writer = csv.writer(sys.stdout)
  writer = UnicodeWriter(sys.stdout)
  writer.writerow(columns)
  for post in posts:
    row =  [post.id, post.publish_date, post.title, post.link, ','.join(post.categories), ','.join(post.tags)]
    writer.writerow(row)
  

if __name__ == '__main__':
  main()