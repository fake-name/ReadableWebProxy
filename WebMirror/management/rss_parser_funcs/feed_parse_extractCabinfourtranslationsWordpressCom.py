def extractCabinfourtranslationsWordpressCom(item):
	'''
	Parser for 'cabinfourtranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('mistake',                'Everything Was a Mistake',                      'translated'),
		('gold spoon',             'The Goal is to Become a Gold Spoon so I Need to be Completely Invulnerable',                      'translated'),
		('happy villainess',       'The Villainess is Happy Today',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False