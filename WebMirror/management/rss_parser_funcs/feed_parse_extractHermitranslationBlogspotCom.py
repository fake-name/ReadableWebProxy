def extractHermitranslationBlogspotCom(item):
	'''
	Parser for 'hermitranslation.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
	if item['tags'] == [] and item['title'].startswith("Chapter "):
			return buildReleaseMessageWithType(item, "My fiancé is in love with my little sister", vol, chp, frag=frag, postfix=postfix)
		
	if len(item['tags']) == 1 and item['tags'][0].lower().startswith("chapter ") and item['title'].startswith("Chapter "):
			return buildReleaseMessageWithType(item, "My fiancé is in love with my little sister", vol, chp, frag=frag, postfix=postfix)
		
		

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False