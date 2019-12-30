def extractRhexSTranslations(item):
	"""
	Parser for 'Rhex's Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Ore no Isekai Shimai ga Jichou Shinai!',     'Ore no Isekai Shimai ga Jichou Shinai!',    'translated'),
		('The Reckless Trap Magician',                 'The Reckless Trap Magician',                'translated'),
		('TRTM',                                       'The Reckless Trap Magician',                'translated'),
		('The Last Surviving Alchemist',               'The Last Surviving Alchemist',              'translated'),
		('Atelier Tanaka',                             'Atelier Tanaka',                            'translated'),
		('Yandere Goddess',                            'Yandere Megami No Hakoniwa',                'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False