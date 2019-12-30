def extractWinterTranslates(item):
	"""
	'Winter Translates'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	if 'Summaries' in item['tags']:
		return None
		
	tagmap = [
		('Villain Rehab Plan',       'Transmigrating into a Mob Character to Rehabilitate the Villain Plan', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False