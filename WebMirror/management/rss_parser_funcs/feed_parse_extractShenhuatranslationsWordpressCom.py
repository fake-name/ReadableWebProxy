def extractShenhuatranslationsWordpressCom(item):
	'''
	Parser for 'shenhuatranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Rebirth of MC',                    'Rebirth of MC',                                                   'translated'), 
		('Qinglian Chronicles',              'Qinglian Chronicles',                                             'translated'), 
		('It\'s Actually Not Easy...',       'It\'s Actually Not Easy Wanting to be a Supporting Male Lead',    'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False