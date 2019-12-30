def extractAlpenGlowTranslations(item):
	"""
	'Alpen Glow Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = {

		'Shu Nv Minglan'                                  : 'The Legend of the Concubine\'s Daughter Minglan',

	}

	for tag, sname in tagmap.items():
		if tag in item['tags']:
			return buildReleaseMessageWithType(item, sname, vol, chp, frag=frag)
			
	return False