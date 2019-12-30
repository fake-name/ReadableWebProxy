def extractCherryclannovelsWordpressCom(item):
	'''
	Parser for 'cherryclannovels.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('I Am An NPC',                                       'I Am An NPC',                                                      'translated'),
		('Sorry, I\'m an NPC',                                'I Am An NPC',                                                      'translated'),
		('Rebirth of the Strongest Female Emperor',           'Rebirth of the Strongest Female Emperor',                          'translated'),
		('Rebirth and Rise: The Campus Business Woman',       'Rebirth and Rise: The Campus Business Woman',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('I Have Medicine [System]',                          'I Have Medicine [System]',                                         'translated'),
		('I Am An NPC',                                       'I Am An NPC',                                                      'translated'),
		('Rebirth of the Strongest Female Emperor',           'Rebirth of the Strongest Female Emperor',                          'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False