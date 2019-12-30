def extractTaekanWordpressCom(item):
	'''
	Parser for 'taekan.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Seiken Tsukai no World Break',       'Seiken Tsukai no World Break',                      'translated'),
		('rakudai kishi no eiyuutan',          'Rakudai Kishi no Cavalry',                          'translated'),
		('Hundred',       'Hundred',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False