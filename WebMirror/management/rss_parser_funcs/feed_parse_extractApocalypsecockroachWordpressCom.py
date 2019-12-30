def extractApocalypsecockroachWordpressCom(item):
	'''
	Parser for 'apocalypsecockroach.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	
	if item['tags'] == ['Uncategorized']:
		try:
			title = item['title']
			if title.startswith("Chapter "):
				title = title[len("Chapter "):]
			int(title)
			return buildReleaseMessageWithType(item, "Apocalypse Cockroach", vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		except Exception:
			pass
		
		
			
	
	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False