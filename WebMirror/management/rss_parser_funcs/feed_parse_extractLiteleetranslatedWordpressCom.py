def extractLiteleetranslatedWordpressCom(item):
	'''
	Parser for 'liteleetranslated.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	tagmap = [
		('My Girlfriend Is A Zombie',       'My Girlfriend Is A Zombie',                      'translated'), 
		('Things From Another World',       'Things From Another World',                      'translated'), 
		('The Sex Contract',       'The Sex Contract, A Naive Short-Tempered Girl',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False