
import database as db
import logSetup

import NUSeriesUpdateFilter

def go():
	logSetup.initLogging()
	print(db.engine)

	fetcher = NUSeriesUpdateFilter.NUSeriesUpdateFilter(db.session())
	print(fetcher)
	# print(fetcher.handlePage("https://www.wlnupdates.com"))
	print(fetcher.handlePage("https://www.novelupdates.com"))


if __name__ == '__main__':
	go()

