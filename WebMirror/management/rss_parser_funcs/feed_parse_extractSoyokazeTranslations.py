def extractSoyokazeTranslations(item):
	'''
	Parser for 'Soyokaze Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	tagmap = {

		'Half-Dragon Slave Life'                             : 'Half-Dragon Slave Life',
		'Hakai Me no Yuuri'                                  : 'Hakai Me no Yuuri',

	}

	for tag, sname in tagmap.items():
		if tag in item['tags']:
			return buildReleaseMessageWithType(item, sname, vol, chp, frag=frag)

	return False