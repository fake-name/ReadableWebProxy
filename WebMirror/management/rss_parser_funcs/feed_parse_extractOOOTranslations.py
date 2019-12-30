def extractOOOTranslations(item):
	"""
	'OOO Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Noble Emblem',        'Noble Emblem',                       'translated'),
		('God Rank Hero',       'God Rank Hero',                      'translated'),
		('Dark Night Ranger',   'Dark Night Ranger',                  'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


		
	return False