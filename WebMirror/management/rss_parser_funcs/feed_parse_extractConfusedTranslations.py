def extractConfusedTranslations(item):
	'''
	Parser for 'Confused Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	tagmap = {
		'Youkoso Jitsuryoku'                      : 'Youkoso Zitsuryoku Shijou Shugi no Kyoushitsu e',
		'Gamers!'                                 : 'Gamers!',
		
	}

	for tag, sname in tagmap.items():
		if tag in item['tags']:
			return buildReleaseMessageWithType(item, sname, vol, chp, frag=frag)


	return False