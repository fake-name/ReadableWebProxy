def extractDarkstarlightsWordpressCom(item):
	'''
	Parser for 'darkstarlights.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	bad = [
			'Princess Agents Portuguese'
		]
	
	if any([tmp in item['tags'] for tmp in bad]):
		return None

	tagmap = [
		('Drunken Exquisiteness',       'Lost Love in Times',                      'translated'),
		('Princess Agents',       'Queen of No. 11 Agent',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False