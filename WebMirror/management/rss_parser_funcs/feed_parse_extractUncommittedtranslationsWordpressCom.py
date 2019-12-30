def extractUncommittedtranslationsWordpressCom(item):
	'''
	Parser for 'uncommittedtranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('I’m Going to Destroy Another World For a Bit Chapters',        'I\'m Going to Destroy Another World For a Bit',                       'translated'), 
		('I Was Made the Disciple of a Yandere Girl But Chapters',       'I was made the disciple of a yandere girl, but',                      'translated'), 
		('I was made the disciple of a yandere girl, but',               'I was made the disciple of a yandere girl, but',                      'translated'), 
		('Evil God Chapter',                                             'Evil God',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False