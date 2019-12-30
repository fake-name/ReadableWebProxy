def extractHainemakorutranslationsBlogspotCom(item):
	'''
	Parser for 'hainemakorutranslations.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if 'news' in item['tags']:
		return None

	tagmap = [
		('10000 STEPS',                                                                  'Level Up Just by Walking. In 10 Thousand Steps It Will Be Level 10000!',                      'translated'),
		('Level Up Just by Walking. In 10 Thousand Steps It Will Be Level 10000!',       'Level Up Just by Walking. In 10 Thousand Steps It Will Be Level 10000!',                      'translated'),
		('Ecstas Online',                                                                'Ecstas Online',                                                                               'translated'),
		('Is He A Hero? Yes',                                                            'Is He A Hero? Yes',                                                                           'translated'),
		('Obtaining the Strongest Cheat',                                                'Obtaining the Strongest Cheat',                                                               'translated'),
		('Humans are the Strongest Race',                                                'Humans are the Strongest Race',                                                               'translated'),
		('Humans are the Strongest Race [LN]',                                           'Humans are the Strongest Race [LN]',                                                          'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False