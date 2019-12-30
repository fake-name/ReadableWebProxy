def extractImjustheretoreadblCom(item):
	'''
	Parser for 'imjustheretoreadbl.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('RAAS',       'Reborn As a System',                                       'translated'),
		('SP',         'Screen Partner',                                           'translated'), 
		('PUP',        'Picked up by the Protagonist of a Tormented! MC Novel',    'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False