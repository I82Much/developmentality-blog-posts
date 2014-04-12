# This script parses the HTML table that contains the Published data for your Wordpress.com blog.
# https://developmentality.wordpress.com/wp-admin/edit.php?post_status=publish&post_type=post&orderby=title&order=asc

from bs4 import BeautifulSoup

def main():
	soup = BeautifulSoup(open("all_posts.html").read())
	print soup

if __name__ == '__main__':
	main()


