def extractHarhartlWordpressCom(item):
	'''
	Parser for 'harhartl.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Sons, Too Mensao',                    'Sons, Too Mensao',                                   'translated'),
		('My Chief Husband, Too Mensao!',       'My Chief Husband, Too Mensao!',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False