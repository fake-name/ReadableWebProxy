def extractHikkinoMoriTranslations(item):
	"""
	# 'Hikki no Mori Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].lower().startswith('chapter') or item['title'].lower().startswith('hyaku ma no shu'):
		return buildReleaseMessageWithType(item, 'Hyaku ma no Shu', vol, chp, frag=frag, postfix=postfix)
		
	tagmap = [
		('Falling In Love With The Villainess',       'Falling In Love With The Villainess',                      'translated'), 
		('FILWTV',       'Falling In Love With The Villainess',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False