def extractAkashiatranslationsWordpressCom(item):
	'''
	Parser for 'akashiatranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('I became the strongest',       'Hazure Waku no 【Joutai Ijou Sukiru】de Saikyou ni Natta Ore ga Subete wo Juurin suru made',                      'translated'),
		('I got stranded',               'Mikai no Wakusei ni Fujichaku Shi ta Kedo Kaere Sou ni Nai node Jingai Harem wo Mezashite mi Masu',               'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False