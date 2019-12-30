def extractSodachipCom(item):
	'''
	Parser for 'sodachip.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Dream Life',            'Dream Life ~Living in an Oneiric Parallel Universe~',                      'translated'), 
		('Trinitas Mundus',       'Trinitas Mundus',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False