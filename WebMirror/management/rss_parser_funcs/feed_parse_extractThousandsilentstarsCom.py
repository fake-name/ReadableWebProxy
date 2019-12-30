def extractThousandsilentstarsCom(item):
	'''
	Parser for 'thousandsilentstars.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('otouto wo suki ni narimashita',       'Otouto wo Suki ni Narimashita',                      'translated'),
		('otoko darake no isekai trip',         'Otoko Darake no Isekai Trip ~BL wa Okotowari~',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False