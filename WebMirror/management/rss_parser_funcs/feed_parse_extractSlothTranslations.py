def extractSlothTranslations(item):
	"""
	Sloth Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Evil Lord',               'I\'m the Evil Lord of an Intergalactic Empire!',                           'translated'),
		('villainous butler',       'The Villainous Daughter\'s Butler ~I Raised Her to be Very Cute~',         'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False