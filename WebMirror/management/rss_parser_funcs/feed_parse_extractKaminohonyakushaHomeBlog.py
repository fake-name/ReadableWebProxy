def extractKaminohonyakushaHomeBlog(item):
	'''
	Parser for 'kaminohonyakusha.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	chp_prefixes = [
			('lv 99999 chapter ',  'Ore wa LV99999, Shikashi, Ore no Tokei ga 1',               'translated'),
			('Lv99999 chapter ',   'Ore wa LV99999, Shikashi, Ore no Tokei ga 1',               'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False