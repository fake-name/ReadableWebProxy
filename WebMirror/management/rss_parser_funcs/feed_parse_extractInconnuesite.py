def extractInconnuesite(item):
	'''
	Parser for 'inconnuesite'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	tagmap = [
		("SGS", "Shoujo Grand Summoning",    'translated'),
		("UAW", "Unlimited Anime Works",     'translated'),
		("HF",  "Holistic Fantasy",          'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False