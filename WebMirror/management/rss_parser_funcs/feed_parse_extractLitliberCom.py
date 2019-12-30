def extractLitliberCom(item):
	'''
	Parser for 'litliber.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Carnival Lights',         'Carnival Lights',                  'oel'),
		('Life Reconstructed',      'Life Reconstructed',               'oel'),
		('North of Happenstance',   'North of Happenstance',            'oel'),
		('Inside Edge',             'The Inside Edge',                  'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False