def extractHinawaryWordpressCom(item):
	'''
	Parser for 'hinawary.wordpress.com'
	'''
	if 'doodles and writing drafts' in item['tags']:
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	if item['tags'] == ['Pork Belly']:
		return buildReleaseMessageWithType(item, 'Pork Belly', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
	if item['tags'] == ['Chapters']:
		return buildReleaseMessageWithType(item, 'The Story of a Small Fox Who Has a Star', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		

	tagmap = [
		('the story of a small fox who has a star',       'The Story of a Small Fox Who Has a Star',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False