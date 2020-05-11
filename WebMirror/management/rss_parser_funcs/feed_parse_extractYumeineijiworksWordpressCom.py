def extractYumeineijiworksWordpressCom(item):
	'''
	Parser for 'yumeineijiworks.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('hagure seirei ino shinsatsu kiroku',                                    'hagure seirei ino shinsatsu kiroku',                                                   'translated'),
		('homeless tensei: isekai de jiyuu sugiru majutsu jisoku seikatsu',       'homeless tensei: isekai de jiyuu sugiru majutsu jisoku seikatsu',                      'translated'),
		('chocolate bliss',                                                       'chocolate bliss',                                                                      'translated'),
		('glitzheria',                                                            'glitzheria',                                                                           'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False