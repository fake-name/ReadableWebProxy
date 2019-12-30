def extractPrinceRevolution(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		

	tagmap = [
		('Romance RPG',                  'Romance RPG',                  'translated'),
		('The Legend of Sun Knight',     'The Legend of Sun Knight',     'translated'),
		('Dominions End',                'Dominions End',                'translated'),
		('½ Prince',                     '½ Prince',                     'translated'),
		('killvsprince',                 'Kill No More VS 1/2 Prince',   'translated'),
		('Illusions-Lies-Truth',         'Illusions, Lies, Truth',       'translated'),
		('No Hero',                      'No Hero',                      'translated'),
		('God',                          'GOD',                          'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False