def extractEternarianovelsCom(item):
	'''
	Parser for 'eternarianovels.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Other World\'s Monster Breeder',       'Other World\'s Monster Breeder',                      'translated'),
		('pokegod',                              'Other World\'s Monster Breeder',                      'translated'),
		('Le Festin de Vampire',                 'Le Festin de Vampire',                                'translated'),
		('I\'m OP, but I Began an Inn',          'Cheat Dakedo Yadoya Hajimemashita.',                  'translated'),
		('PRC',                                  'PRC',                                                 'translated'),
		('Loiterous',                            'Loiterous',                                           'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False