def extractZhanlantranslationsWordpressCom(item):
	'''
	Parser for 'zhanlantranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Online Game: Willingly Captured',                                        'Online Game: Willingly Captured',                                                       'translated'), 
		('I Am A Killer',                                                          'I Am A Killer',                                                                         'translated'), 
		('Endless Love',                                                           'Endless Love',                                                                          'translated'), 
		('My Classmate Is Two Hundred Million Years Old',                          'My Classmate Is Two Hundred Million Years Old',                                         'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False