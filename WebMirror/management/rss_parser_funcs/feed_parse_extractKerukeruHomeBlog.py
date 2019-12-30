def extractKerukeruHomeBlog(item):
	'''
	Parser for 'kerukeru.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None


	if item['tags'] == ['Uncategorized'] and item['title'].startswith("Chapter "):
		return buildReleaseMessageWithType(item, "I decided to cook because the losing potion was soy sauce ", vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False