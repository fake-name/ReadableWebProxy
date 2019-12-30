def extractFutileStruggle(item):
	'''
	Parser for 'Futile Struggle'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	tagmap = {

		'Kanna no Kanna'                                  : 'Kanna no Kanna',

	}

	for tag, sname in tagmap.items():
		if tag in item['tags']:
			return buildReleaseMessageWithType(item, sname, vol, chp, frag=frag)

	return False