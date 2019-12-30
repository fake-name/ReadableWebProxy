def extractPotatotranslationCom(item):
	'''
	Parser for 'potatotranslation.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Saint Dragon Totem',   'Saint Dragon Totem',                  'translated'), 
		('Super God Gene',       'Super God Gene',                      'translated'), 
		('Master feels stifled', 'Master feels stifled',                'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False