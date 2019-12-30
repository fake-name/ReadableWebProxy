def extractHaraguroscansBlogspotCom(item):
	'''
	Parser for 'haraguroscans.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	if 'Manga' in item['tags']:
		return None
		
	tagmap = [
		('GJ-Bu',       'GJ Bu',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False