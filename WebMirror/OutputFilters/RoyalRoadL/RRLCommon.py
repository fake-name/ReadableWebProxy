



import json
import os.path
import cachetools



MIN_RATING_STARS = 2.5

# * 2 to convert from stars to 0-10 range actually used
MIN_RATING_FLOAT = MIN_RATING_STARS * 2
MIN_RATE_CNT     = 3
MIN_CHAPTERS     = 4


@cachetools.cached(cachetools.TTLCache(100, 60*5))
def load_lut():
	outf = os.path.join(os.path.split(__file__)[0], 'royal_roadl_overrides.json')
	with open(outf) as fp:
		lut = json.load(fp)

	assert 'force_sequential_numbering' in lut

	return lut

def fix_tag(tagtxt):
	# This is literally only tolerable since load_lut is memoized
	conf = load_lut()

	if tagtxt in conf['tag_rename']:
		tagtxt = conf['tag_rename'][tagtxt]
	return tagtxt


def check_fix_numbering(log, releases, series_id):

	conf = load_lut()

	must_renumber = series_id in conf['force_sequential_numbering']

	missing_chap = 0
	for item in releases:
		if not (item['vol'] or item['chp']):
			missing_chap += 1

	if releases:
		unnumbered = (missing_chap/len(releases)) * 100
		if (len(releases) >= 5 and unnumbered > 80) or must_renumber:
			if must_renumber:
				log.warning("Item numbering force-overridden! Adding simple sequential chapter numbers.")
			else:
				log.warning("Item seems to not have numbered chapters. Adding simple sequential chapter numbers.")
			chap = 1
			for item in releases:
				item['vol'] = None
				item['chp'] = chap
				chap += 1

	return releases
