def extractFuyunekoWordpressCom(item):
	'''
	Parser for 'fuyuneko.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Wu Gate',              'The Crazy Adventures of Wu Gate',                      'translated'),
		('Meow Meow Meow',       'Meow Meow Meow',                                       'translated'),
		('chongfei manual',      'Chongfei Manual',                                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('Meow Meow Meow Ch ',       'Meow Meow Meow',                                       'translated'),
		('ChongFei Manual Ch ',      'Chongfei Manual',                                      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False