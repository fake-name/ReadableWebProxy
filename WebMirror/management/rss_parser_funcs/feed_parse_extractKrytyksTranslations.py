def extractKrytyksTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Only Sense Online',          'Only Sense Online',    'translated'),
		('AntiMagic Academy',          'AntiMagic Academy',    'translated'),
		('Daybreak on Hyperion',       'Daybreak on Hyperion', 'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False