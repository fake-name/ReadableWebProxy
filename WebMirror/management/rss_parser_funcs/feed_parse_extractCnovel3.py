def extractCnovel3(item):
	"""
	Parser for 'Cnovel <3'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('scum villain system',       'The Scum Villain\'s Self-Saving System',                      'translated'),
		('Demon King',                'Demon King: The Parting of Orchid and Cang',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False