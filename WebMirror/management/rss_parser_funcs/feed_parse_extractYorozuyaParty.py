def extractYorozuyaParty(item):
	'''
	Parser for 'yorozuya.party'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	#  and 

	tagmap = [
		('eijiw',       'Everywhere in Jianghu is Wonderful',                      'translated'),
		('dwgl',        'Di Wang Gong Lue',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False