def extractBcat00(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	titlemap = [
		('Overturning the Heavens chapter', 'Overturning the Heavens',                                                           'translated'),
		('Law of the devil',                'Law of the Devil',                                                                  'translated'),
		('Miracle doctor',                  'Miracle Doctor, Abandoned Daughter: The Sly Emperor\'s Wild Beast-Tamer Empress',   'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False