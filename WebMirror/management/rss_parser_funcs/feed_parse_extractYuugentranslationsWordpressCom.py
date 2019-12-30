def extractYuugentranslationsWordpressCom(item):
	'''
	Parser for 'yuugentranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('Yandere Imouto – ', 'Confinement by my Yandere Imouto',                                         'translated'),
		('Battleship AI – ',  'Unparalleled Path ~ Reincarnated as the AI for a space battleship ~',      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False