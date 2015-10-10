

import WebMirror.util.webFunctions as webFunctions
import WebMirror.database as db
import WebMirror.util.urlFuncs as urlFuncs

class StoriesOnlineFetch(object):

	def __init__(self):
		print("StoriesOnlineFetch __init__()")
		self.log = logging.getLogger("Main.Text.StoriesOnline")
		super().__init__()
		self.wg = webFunctions.WebGetRobust()

		self.initializeStartUrls()

	def initializeStartUrls(self):
		print("Initializing all start URLs in the database")

		for x in range(100000):
			starturl = "http://storiesonline.net/s/{num}/".format(num=x)
			# have = db.get_session().query(db.WebPages) \
			# 	.filter(db.WebPages.url == starturl)   \
			# 	.count()
			# if not have:
			netloc = urlFuncs.getNetLoc(starturl)
			new = db.WebPages(
					url               = starturl,
					starturl          = starturl,
					netloc            = netloc,
					type              = "western",
					priority          = db.DB_IDLE_PRIORITY,
					distance          = db.DB_DEFAULT_DIST,
					normal_fetch_mode = False,
				)
			print("Missing start-url for address: '{}'".format(starturl))
			db.get_session().add(new)

			if x % 5000 == 0:
				print("Committing")
				db.get_session().commit()
		db.get_session().commit()
