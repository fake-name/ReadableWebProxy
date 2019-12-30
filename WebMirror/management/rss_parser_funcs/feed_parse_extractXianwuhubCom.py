def extractXianwuhubCom(item):
	'''
	Parser for 'xianwuhub.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('WDDG',                                 'World Defying Dan God',                      'translated'),
		('Everlasting Immortal Firmament',       'Everlasting Immortal Firmament',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('WDDG Chapter',      'World Defying Dan God',                      'translated'),
		('EIF Chapter',       'Everlasting Immortal Firmament',             'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False