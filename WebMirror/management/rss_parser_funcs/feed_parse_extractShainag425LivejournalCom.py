def extractShainag425LivejournalCom(item):
	'''
	Parser for 'shainag425.livejournal.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
	if item['tags'] == [] and item['title'].startswith("CHAPTER "):
		return buildReleaseMessageWithType(item, "Rebirth of the Tyrant's Pet: Regent Prince is too fierce", vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False