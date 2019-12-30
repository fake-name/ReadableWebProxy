def extractAlbedo404BlogspotCom(item):
	'''
	Parser for 'albedo404.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	if item['tags'] != []:
		return None
	
	
	if re.match("Ch \d+ Tondemo Skill de Isekai Hourou Meshi", item['title'], re.IGNORECASE):
			return buildReleaseMessageWithType(item, 'Tondemo Skill de Isekai Hourou Meshi', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		
	
	
	if re.match("Ch \d+ Sakyubasu ni Tensei Shita no de Miruku o Shiborimasu", item['title'], re.IGNORECASE):
			return buildReleaseMessageWithType(item, 'Sakyubasu ni Tensei Shita no de Miruku o Shiborimasu', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		
		

	return False