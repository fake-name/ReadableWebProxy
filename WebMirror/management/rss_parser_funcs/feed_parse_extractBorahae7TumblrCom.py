def extractBorahae7TumblrCom(item):
	'''
	Parser for 'borahae7.tumblr.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	# Don't generate false parses on the series "the strongest prophet who had trained 100 heroes is admired by his apprentices around the world even as an adventurer"
	if (vol, chp, frag) == (None, 100, 0):
		return None

	tagmap = [
		('fbcbtr tl',       'Fiancee Be Chosen By The Ring',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False