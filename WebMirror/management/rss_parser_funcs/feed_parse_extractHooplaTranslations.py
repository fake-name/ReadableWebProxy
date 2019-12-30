def extractHooplaTranslations(item):
	'''
	Parser for 'Hoopla Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	

	tagmap = {

		"Mushoku Tensei Redundancy Chapters"                     :  "Mushoku Tensei Redundancy",
		"Mushoku Tensei Redundancy Chapters TL"                  :  "Mushoku Tensei Redundancy",

	}

	for tag, sname in tagmap.items():
		if tag in item['tags']:
			return buildReleaseMessageWithType(item, sname, vol, chp, frag=frag)



	return False