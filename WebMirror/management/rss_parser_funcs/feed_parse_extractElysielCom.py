def extractElysielCom(item):
	'''
	Parser for 'elysiel.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Reincarnated Swordmaster',                                   'Reincarnated Swordmaster',                                                  'translated'),
		('Green Skin',                                                 'Green Skin',                                                                'translated'),
		('Dragon Poor',                                                'Dragon Poor',                                                               'translated'),
		('Max Level His Majesty in Moorim',                            'Max Level His Majesty in Moorim',                                           'translated'),
		('PRC',                                                        'PRC',                                                                       'translated'),
		('Loiterous',                                                  'Loiterous',                                                                 'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False