def extractMyEngTranslation(item):
	"""
	MyEngTranslation
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	

	
	tagmap = [
		('Don\'t Read this Novel',       'Don\'t Read this Novel',                      'translated'),
		('Gantung',                      'Gantung',                                     'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if item['tags'] != ['Uncategorized']:
		return False

	
	if 'sasar' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Sasar', vol, chp, frag=frag, postfix=postfix)
	
	# Only assume a release if the title is entirely numeric
	try:
		int(item['title'])
		return buildReleaseMessageWithType(item, 'Gantung', vol, chp, frag=frag, postfix=postfix)
	except ValueError:
		pass
		
	
	return False