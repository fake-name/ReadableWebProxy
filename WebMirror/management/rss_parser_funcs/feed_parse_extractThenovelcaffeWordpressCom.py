def extractThenovelcaffeWordpressCom(item):
	'''
	Parser for 'thenovelcaffe.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('ptma',       'Please Throw Me Away',                      'translated'),
		('tsrbtratbp',       'The Symbiotic Relationship Between the Rabbit and the Black Panther',                      'translated'),
		('tsrbrbp',       'The Symbiotic Relationship Between the Rabbit and the Black Panther',                      'translated'),
		('itliwl',       'In This Life, I Will be the Lord',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False