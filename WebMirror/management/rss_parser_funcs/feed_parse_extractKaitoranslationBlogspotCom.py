def extractKaitoranslationBlogspotCom(item):
	'''
	Parser for 'kaitoranslation.blogspot.com'
	'''
	
	if not item['title'].lower().startswith('[eng]'):
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Keizoku wa Maryoku Nari',       'Keizoku wa Maryoku Nari',                      'translated'),
		('nido tensei',                   'Nido Tensei Shita Shounen wa S Rank Boukensha Toshite Heion ni Sugosu ~ Zense ga kenja de eiyūdatta boku wa raisede wa jimi ni ikiru ~',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False