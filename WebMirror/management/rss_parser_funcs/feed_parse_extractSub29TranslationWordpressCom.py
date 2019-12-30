def extractSub29TranslationWordpressCom(item):
	'''
	Parser for 'sub29translation.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Earth Dragon Dungeon',       'Earth Dragon Dungeon',                      'translated'), 
		('Doll Dungeon',               'Doll Dungeon',                              'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False