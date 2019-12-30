def extractSinnesspielDreamwidthOrg(item):
	'''
	Parser for 'sinnesspiel.dreamwidth.org'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	
	
	res = re.search(r"Shiki Novel Translations (\d+)\.(\d+)\.(\d+)", item['title'])
	
	if res:
		vol, chp, frag = res.group(1), res.group(2), res.group(3)
		
		
	if not (chp or vol) or "preview" in item['title'].lower():
		return False


	tagmap = [
		('shiki',     'Shiki',                    'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False