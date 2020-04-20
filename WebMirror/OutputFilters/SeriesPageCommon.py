



import json
import os.path
import cachetools



MIN_RATING_STARS = 2.5

# * 2 to convert from stars to 0-10 range actually used
MIN_RATING_FLOAT = MIN_RATING_STARS * 2
MIN_RATE_CNT     = 3
MIN_CHAPTERS     = 4


@cachetools.cached(cachetools.TTLCache(100, 60*5))
def _load_lut_internal():
	outf = os.path.join(os.path.split(__file__)[0], 'series_overrides.json')
	with open(outf) as fp:
		cont = fp.read()

	lut = json.loads(cont)

	return lut

def get_rrl_lut():

	lut = _load_lut_internal()
	lut = lut['royalroadl']

	assert 'force_sequential_numbering' in lut
	return lut

def get_sh_lut():

	lut = _load_lut_internal()
	lut = lut['scribblehub']

	return lut

def fix_tag(tagtxt):
	# This is literally only tolerable since load_lut is memoized
	conf = _load_lut_internal()

	if tagtxt in conf['tag_rename']:
		tagtxt = conf['tag_rename'][tagtxt]
	return tagtxt


def fix_genre(genretxt):
	# This is literally only tolerable since load_lut is memoized
	conf = _load_lut_internal()

	if genretxt in conf['genre_rename']:
		genretxt = conf['genre_rename'][genretxt]
	return genretxt


def clean_tag(in_txt):
	assert isinstance(in_txt, str), "Passed item is not a string! Type: '%s' -> '%s'" % (type(in_txt), in_txt, )
	assert not "," in in_txt, "It looks like a tag list got submitted as a tag! String: '%s'" % (in_txt, )
	in_txt = in_txt.strip().lower().replace(" ", "-")
	return in_txt

def check_fix_numbering(log, releases, series_id, rrl=False, sh=False):

	assert rrl or sh
	assert sum([rrl, sh]) == 1

	if not isinstance(series_id, str):
		log.warning("Series id is not a string: %s -> %s", series_id, type(series_id))
		assert isinstance(series_id, (str, int))
		series_id = str(series_id)

	if rrl:
		conf = get_rrl_lut()
	elif sh:
		conf = get_sh_lut()

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

def test():
	get_rrl_lut()

if __name__ == "__main__":
	test()
