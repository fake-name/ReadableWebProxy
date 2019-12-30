def extractBreakingOffTheEngagementBringItOn(item):
	'''
	Parser for 'Breaking off the engagement .. Bring it on!'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		("Breaking off the engagement .. Bring it on!",       'Breaking off the engagement .. Bring it on!',               'translated'),
		# ("Wizard's Soul 〜恋の聖戦〜",                        'Wizard\'s Soul ~Holy War of Love~',                         'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False