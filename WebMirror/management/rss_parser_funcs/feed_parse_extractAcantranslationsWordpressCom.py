def extractAcantranslationsWordpressCom(item):
	'''
	Parser for 'acantranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('After defeating the Demon Lord, he became Guild Master',       'After defeating the Demon Lord, he became Guild Master',                                       'translated'),
		('Welcome to the Monsters Guild!',                               'Welcome to the Monsters\' Guild ~ The Strongest Group Who Did Everything, for a Price ~',      'translated'),
		('A New Game from the Depths of Captivity!',                     'A New Game from the Depths of Captivity!',                                                     'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False