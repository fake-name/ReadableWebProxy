def extractAsplashofnovelsWordpressCom(item):
	'''
	Parser for 'asplashofnovels.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	urlfrag = [
		('/cool-goddess-special-agent-chapter-',  'Cool Goddess Special Agent',     'translated'),
		('http://www.rebirth.online/novel/jintetsu/',  'Jintetsu',     'translated'),

		('rebirth.online/novel/earths-core' ,          "Earth's Core", 'oel'),
	]

	for key, name, tl_type in urlfrag:
		if key in item['linkUrl'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False