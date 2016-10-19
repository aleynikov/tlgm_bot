import ConfigParser
import mysql.connector
import pytumblr
import dropbox

def test_mysql():
	cfg = ConfigParser.ConfigParser()
	cfg.read('mysql.cfg')

	try:
		cnx = mysql.connector.connect(user=cfg.get('client', 'user'),
			password=cfg.get('client', 'password'),
			host=cfg.get('client', 'host'),
			database=cfg.get('client', 'database'))

		cursor = cnx.cursor()
		cursor.execute("select * from user")

		for (fname, lname, age) in cursor:
			print "{} {} - {} age".format(fname, lname, age)

	except mysql.connector.Error as err:
		print err
	else:
		cnx.close()

def test_tumblr():
	cfg = ConfigParser.ConfigParser()
	cfg.read('tumblr.cfg')

	client = pytumblr.TumblrRestClient(consumer_key=cfg.get('api', 'consumer_key'),
		consumer_secret=cfg.get('api', 'consumer_secret'),
		oauth_token=cfg.get('api', 'oauth_token'),
		oauth_secret=cfg.get('api', 'oauth_secret'));
	print client.info()

def test_dropbox():
	cfg = ConfigParser.ConfigParser()
	cfg.read('dropbox.cfg')

	dbx = dropbox.Dropbox(cfg.get('api', 'access_token'))
	print dbx.users_get_current_account()

def main():
	print 'Test mysql connection...\n'
	test_mysql()

	print 'Test tumblr client...\n'
	test_tumblr()

	print 'Test dropbox client...\n'
	test_dropbox()

if __name__ == '__main__':
	main()