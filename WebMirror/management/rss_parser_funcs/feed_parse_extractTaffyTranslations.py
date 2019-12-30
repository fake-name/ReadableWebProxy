def extractTaffyTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
		
		
	tagmap = [
		('CCM',               'Close Combat Mage',                 'translated'),
		('CC',                'Cheating Craft',                    'translated'),
		('KSM',               'Key of Sunken Moon',                'translated'),
		('YBCB',              'Yu Brothers\' Case Book',           'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
		
	return False