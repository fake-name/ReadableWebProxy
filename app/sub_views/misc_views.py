
from flask import g
from flask import render_template
from flask import request

from app import app


import urllib.parse
import WebMirror.rules

from WebMirror import rules
import common.global_constants
import RawArchiver.RawActiveModules


def getBadWords(ruleset, netloc):
	badwords = [tmp for tmp in common.global_constants.GLOBAL_BAD_URLS]
	for item in [rules for rules in ruleset if rules['netlocs'] and netloc in rules['netlocs']]:
		badwords += item['badwords']

	# A "None" can occationally crop up. Filter it.
	badwords = [badword for badword in badwords if badword]
	badwords = [badword.lower() for badword in badwords]
	badwords = list(set(badwords))

	badcompounds = []

	for item in [rules for rules in ruleset if rules['netlocs'] and netloc in rules['netlocs']]:
		if item['compound_badwords']:
			badcompounds += item['compound_badwords']

	return badwords, badcompounds


def isFiltered(link, badwords, badcompounds):
	if link.startswith("data:"):
		return True
	linkl = link.lower()
	if any([badword in linkl for badword in badwords]):
		return True

	if any([all([badword in linkl for badword in badcompound]) for badcompound in badcompounds]):
		print("Compound Filtered:", link, [badword for badword in badwords if badword in linkl ])
		return True

	return False

def get_random_url_group(num_items):
	dat = g.session.execute('''SELECT url FROM web_pages TABLESAMPLE SYSTEM(:percentage) ORDER BY url;''', {'percentage' : num_items})
	dat = list(dat)

	ruleset = rules.load_rules(override=True)

	ret = []
	for linkurl, in dat:
		nl = urllib.parse.urlparse(linkurl).netloc

		badwords, badcompounds = getBadWords(ruleset, nl)
		filtered = isFiltered(linkurl, badwords, badcompounds)

		ret.append((linkurl, filtered))


	return ret

def raw_url_filtered(url):

	for module in RawArchiver.RawActiveModules.ACTIVE_MODULES:
		if module.cares_about_url(url):
			return False
	return True



def get_random_raw_url_group(num_items):
	dat = g.session.execute('''SELECT url FROM raw_web_pages TABLESAMPLE SYSTEM(:percentage) ORDER BY url;''', {'percentage' : num_items})
	dat = list(dat)


	ret = []
	for linkurl, in dat:
		filtered = raw_url_filtered(linkurl)

		ret.append((linkurl, filtered))


	return ret


@app.route('/random-urls/', methods=['GET'])
def random_urls_view():
	entries = get_random_url_group(0.007)

	return render_template('misc/random-urls.html',
		header    = "Random URL Subset",
						   results   = entries,
						   )

@app.route('/random-raw-urls/', methods=['GET'])
def random_raw_urls_view():
	entries = get_random_raw_url_group(0.01)

	return render_template('misc/random-urls.html',
		header    = "Random URL Subset",
						   results   = entries,
						   )
