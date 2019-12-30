def extractProcrastinationtranslationWeeblyCom(item):
	'''
	Parser for 'procrastinationtranslation.weebly.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Antelope and Night Wolf - 小羚羊与夜太狼',                                       'The Antelope and Night Wolf',                      'translated'),
		('Love Stops Rumours - 谣言止于恋爱',                                                  'Love Stops Rumours',                               'translated'),
		('&#35875;&#35328;&#27490;&#20110;&#24651;&#29233; &#65293; Love Stops Rumours',       'Love Stops Rumours',                               'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False