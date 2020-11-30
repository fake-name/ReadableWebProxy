def extractRadlaneWebsite(item):
	'''
	Parser for 'radlane.website'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Toaru Ossan no VRMMO katsudouki',              'Toaru Ossan no VRMMO katsudouki',                             'translated'),
		('[novel]toaru ossan no vrmmo katsudouki',       '[novel]toaru ossan no vrmmo katsudouki',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False