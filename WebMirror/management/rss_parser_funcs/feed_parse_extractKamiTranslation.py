def extractKamiTranslation(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	
	if 'Manga' in item['tags']:
		return None
	if 'Anime' in item['tags']:
		return None
	if '4-KOMA' in item['tags']:
		return None
	if 'Non Non Biyori' in item['tags']:
		return None
	if 'Servant X Service' in item['tags']:
		return None
	
	tagmap = [
		('Game Sensou', 'Boku to Kanojo no Game Sensou',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False