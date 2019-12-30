def extractSirmetathysttranslationsHomeBlog(item):
	'''
	Parser for 'sirmetathysttranslations.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('~ Unparalleled Path ~ Reincarnated as the AI for a space battleship',       '~ Unparalleled Path ~ Reincarnated as the AI for a space battleship',                      'translated'),
		('Succubus-san’s Life in Another World',                                      'Succubus-san\'s Life in Another World',                                                    'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False