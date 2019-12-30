def extractChauffeurTranslations(item):
	"""
	'Chauffeur Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = {
		'Hyaku ma no Shu'                                  : 'Hyaku ma no Shu',
	}

	for tag, sname in tagmap.items():
		if tag in item['tags']:
			return buildReleaseMessageWithType(item, sname, vol, chp, frag=frag)
		
	return False