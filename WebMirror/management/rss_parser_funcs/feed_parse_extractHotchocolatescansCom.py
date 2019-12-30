def extractHotchocolatescansCom(item):
	'''
	Parser for 'hotchocolatescans.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	bad_tags = [
			'Yahari Ore no Seishun Rabukome wa Machigatte Iru. - Mougenroku',
			'D-frag',
			'Beastars',
			'The Legend of Zelda: Twilight Princess',
			'Watashi no Shounen',
			'Konjiki no Moji Tsukai',
		]
	
	if any([tag in item['tags'] for tag in bad_tags]):
		return None
		
	
	if "hotchocolatescans.com/fs/download/" in item['contents']:
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False