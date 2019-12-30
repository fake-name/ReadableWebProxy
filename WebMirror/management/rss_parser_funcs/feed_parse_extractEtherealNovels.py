def extractEtherealNovels(item):
	'''
	Parser for 'Ethereal Novels'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	tagmap = {

		'Miracle Doctor, Wild Empress: Genius Summoner'                                  : 'Miracle Doctor, Wild Empress: Genius Summoner',

	}

	for tag, sname in tagmap.items():
		if tag in item['tags']:
			return buildReleaseMessageWithType(item, sname, vol, chp, frag=frag)

	return False