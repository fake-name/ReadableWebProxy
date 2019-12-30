def extractNovelexpressWordpressCom(item):
	'''
	Parser for 'novelexpress.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('RGG',       'Rebirth Of The General\'s Granddaughter',            'translated'),
		('MBH',       'My Beastly Husband',                                 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False