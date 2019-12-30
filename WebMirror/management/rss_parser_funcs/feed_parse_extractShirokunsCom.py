def extractShirokunsCom(item):
	'''
	Parser for 'shirokuns.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Living in this World with Cut & Paste',                                            'Living in this World with Cut & Paste',                                                           'translated'), 
		('Although I am only level 1, but with this unique skill, I am the strongest',       'Although I Am Only Level 1, but with This Unique Skill, I Am the Strongest',                      'translated'), 
		('The whole class was transported to a different world except for me',               'My Entire Class Was Summoned to Another World except for Me',                                     'translated'), 
		('Fantasy falls',                                                                    'Fantasy Falls',                                                                                   'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False