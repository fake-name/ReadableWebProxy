def extractKaitozeroWordpressCom(item):
	'''
	Parser for 'kaitozero.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	print(item)
	if item['title'].startswith("Nukoduke!"):
		return None
	if item['title'].lower().startswith("road to bath"):
		return None
	
	tagmap = [
		('Sokuhi Shigan! (Novel)',       'Sokuhi Shigan!',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False