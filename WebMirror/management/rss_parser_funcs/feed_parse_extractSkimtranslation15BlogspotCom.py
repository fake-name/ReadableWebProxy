def extractSkimtranslation15BlogspotCom(item):
	'''
	Parser for 'skimtranslation15.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
		
	if item['tags'] == []:
		try:
			nums = item['title'].split(" ")[0]
			num = float(nums)
			return buildReleaseMessageWithType(item, "I Got One Star, so I Will Do It", vol, chp, frag=frag, postfix=postfix)
		except ValueError:
			pass
			

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False