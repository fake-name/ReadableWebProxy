def extractInsidethemirrorTumblrCom(item):
	'''
	Parser for 'insidethemirror.tumblr.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('sheisthprotagonist',               'She is the Protagonist',                      'translated'),
		('sheistheprotagonist',              'She is the Protagonist',                      'translated'),
		('rebirthofthegoldenmarriage',       'Rebirth of The Golden Marriage',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False