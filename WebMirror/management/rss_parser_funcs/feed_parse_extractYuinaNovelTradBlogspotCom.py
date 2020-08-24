def extractYuinaNovelTradBlogspotCom(item):
	'''
	Parser for 'yuina-novel-trad.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('since i was reborn as saito yoshiryu i\'m aiming to hand over the territory to oda nobunaga and live longer!',       'Since I Was Reborn as Saito Yoshiryu, I\'m Aiming to Hand Over the Territory to Oda Nobunaga and Live Longer!',                      'translated'),
		('paladin of the end',       'paladin of the end',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False