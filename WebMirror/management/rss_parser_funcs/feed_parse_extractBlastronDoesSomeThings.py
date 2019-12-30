def extractBlastronDoesSomeThings(item):
	"""
	Parser for 'Blastron Does Some Things'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('honzuki no gekokujou',       'honzuki no gekokujou',                      'translated'),
		('kumo desu ga nani ka',       'kumo desu ga nani ka',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False