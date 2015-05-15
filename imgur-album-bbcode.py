import argparse
import re

from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

# Generate BBCode for forums from an Imgur album

def main():
	parser = argparse.ArgumentParser(description="Generate BBCode from an Imgur album")
	parser.add_argument("-c", "--clientid", help="Imgur client ID", required=True)
	parser.add_argument("-s", "--secret", help="Imgur secret", required=True)
	parser.add_argument("-a", "--album", help="Album ID", required=True)

	args = parser.parse_args()

	client = ImgurClient(args.clientid, args.secret)

	try:
		album = client.get_album(args.album)
	except ImgurClientError as e:
		print "Error fetching album - %s:" % (e.status_code)
		print e.error_message
		exit()

	print '[B][SIZE="4"]%s[/SIZE][/B]' % (album.title)

	thumb_regex = re.compile(r"^(.*)\.(.{3,4})$")

	for img in album.images:
		if img['title']:
			print '[SIZE="3"]%s[/SIZE]\n' % (img['title'])
		# Use "large thumbnail" size
		print '[IMG]%s[/IMG]' % (thumb_regex.sub("\\g<1>l.\\2", img['link']))
		description = img['description'] if img['description'] else ""
		print description
		print

if __name__ == "__main__":
	main()