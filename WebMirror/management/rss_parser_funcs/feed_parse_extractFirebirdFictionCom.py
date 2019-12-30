def extractFirebirdFictionCom(item):
	'''
	Parser for 'firebird-fiction.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None


	if 'Haventon Chronicles' in item['tags'] and 'Lord of the Wolves' in item['title']:
		vol = 2
		return buildReleaseMessageWithType(item, "Haventon Chronicles", vol, chp, frag=frag, postfix=postfix, tl_type='oel')
			
	tagmap = [
		('Lawgiver\'s Blade', 'Lawgiver\'s Blade',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

			
	return False