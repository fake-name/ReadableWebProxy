def extractWwwMiraslationNet(item):
	'''
	Parser for 'www.miraslation.net'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('BoukenshaLicense',       'Boukensha License o Hakudatsu Sareta Ossan Dakedo, Manamusume ga Dekita no de Nonbiri Jinsei o Oka Suru',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False