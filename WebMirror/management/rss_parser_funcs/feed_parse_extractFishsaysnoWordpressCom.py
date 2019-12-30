def extractFishsaysnoWordpressCom(item):
	'''
	Parser for 'fishsaysno.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Reborn Otaku\'s Code of Practice for the Apocalypse',       'The Reborn Otaku\'s Code of Practice for the Apocalypse',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('sister of bl', 'I Swear my Brother’s the Protagonist of a BL Manga',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False