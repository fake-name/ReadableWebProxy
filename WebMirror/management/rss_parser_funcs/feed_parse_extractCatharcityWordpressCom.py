def extractCatharcityWordpressCom(item):
	'''
	Parser for 'catharcity.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
		
	tagmap = [
		('Love in Another Life',                        'Love in Another Life: My Gentle Tyrant',                      'translated'),
		('Ballad of Ten Thousand Gu',                   'Ballad of Ten Thousand Gu',                                   'translated'),
		('One Night, One Day, One Year, One Lifetime',  'One Night, One Day, One Year, One Lifetime',                  'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False