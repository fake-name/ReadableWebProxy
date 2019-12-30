def extractTryTranslationsTheBusyOne(item):
	"""
	TryTranslations/The Busy One
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Strategist Knows Everything',       'Gunshi wa Nandemo Shitteiru',                      'translated'), 
		('Jobless',       'I, without possessing a job, aim to become an adventurer!',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False