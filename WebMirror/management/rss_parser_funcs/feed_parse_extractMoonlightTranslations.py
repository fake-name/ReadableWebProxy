def extractMoonlightTranslations(item):
	"""
	Moonlight Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Discovering my Disciple Wants to Eat Me After Raising Him',       'Discovering my Disciple Wants to Eat Me After Raising Him',                      'translated'), 
		('The Promotion Record of A Crown Princess',       'The Promotion Record of A Crown Princess',                      'translated'), 
		('Reborn as My Love Rival\'s Wife',                'Reborn as My Love Rival\'s Wife',                               'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	return False