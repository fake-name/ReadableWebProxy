def extractChestnuttranslationsWordpressCom(item):
	'''
	Parser for 'chestnuttranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Rebirth of the Rich and Wealthy',       'Rebirth of the Rich and Wealthy',                      'translated'),
		('rebirth',                               'Rebirth of the Rich and Wealthy',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False