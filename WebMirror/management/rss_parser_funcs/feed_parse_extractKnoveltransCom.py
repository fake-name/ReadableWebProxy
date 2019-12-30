def extractKnoveltransCom(item):
	'''
	Parser for 'knoveltrans.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Mightiest Manager', 'The Mightiest Manager',                'translated'), 
		('The Skill Maker',       'The Skill Maker',                      'translated'), 
		('Dungeon Maker',         'Dungeon Maker',                        'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False