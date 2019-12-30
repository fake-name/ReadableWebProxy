def extractCobaSemuanyaBlogspotCom(item):
	'''
	Parser for 'coba-semuanya.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
	if 'Game' in item['tags']:
		return None
	if 'Bahasa Indonesia' in item['title']:
		return None
	if 'BahasaIndonesia' in item['title']:
		return None
		

	tagmap = [
		('Goblin Kingdom',       'Goblin Kingdom',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False