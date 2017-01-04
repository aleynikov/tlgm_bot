import ConfigParser
import requests
import hashlib
import os
import time

import pytumblr
import dropbox

def get_top_photos(limit):
	config = ConfigParser.ConfigParser()
	config.read('cfg/tumblr.cfg')

	client = pytumblr.TumblrRestClient(consumer_key=config.get('api', 'consumer_key'),
		consumer_secret=config.get('api', 'consumer_secret'),
		oauth_token=config.get('api', 'oauth_token'),
		oauth_secret=config.get('api', 'oauth_secret'));

	posts = client.posts(blogname=config.get('blogs', 'name'),
		type="photo",
		tag="boobs",
		limit=limit)

	links = []

	for post in posts['posts']:
		photos = post['photos']

		for photo in photos:
			# collect origin photo url
			links.append(photo['original_size']['url'])

	return links

def photo_download(photo_url):
	response = requests.get(photo_url)

	tmp_path = os.path.abspath('tmp/')

	if response.status_code == 200:
		filename = hashlib.md5(photo_url).hexdigest()
		filepath = "{}/{}.jpg".format(tmp_path, filename)

		f = open(filepath, 'wb')
		f.write(response.content)
		f.close()

		return dict(filename=filename, filepath=filepath)

	return None

def photo_upload(filename, filepath):
	config = ConfigParser.ConfigParser()
	config.read('cfg/dropbox.cfg')

	foldername = time.strftime(config.get('folder_settings', 'time_format'))
	folderpath = "/" + foldername

	dbx = dropbox.Dropbox(config.get('api', 'access_token'))
	#dbx.files_create_folder(foldername)

	dbx.files_upload(f=open(filepath, 'rb'),
		path="{}/{}.jpg".format(folderpath, filename));

	os.remove(filepath)

def collect(photo_limit):
	links = get_top_photos(photo_limit)

	for photo_url in links:
		result = photo_download(photo_url)

		if result != None:
			photo_upload(filename=result['filename'],
				filepath=result['filepath'])