def extractKtlchamberWordpressCom(item):
	'''
	Parser for 'ktlchamber.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('God of Music',       'God of Music',                      'translated'),
		('Possessing Nothing', 'Possessing Nothing',                'translated'),
		('One Man Army',       'One Man Army',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False