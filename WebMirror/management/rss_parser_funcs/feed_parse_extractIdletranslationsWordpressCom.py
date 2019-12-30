def extractIdletranslationsWordpressCom(item):
	'''
	Parser for 'idletranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Kaifuku Jutsushi no Yarinaoshi',       'Kaifuku Jutsushi no Yarinaoshi ~ Sokushi Mahou to Skill Copy no Choetsu Heal',      'translated'), 
		('Nagai Koto',                           'Nagai Koto',                                                                        'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False