def extractTheWorldOnTheOtherSide(item):
	"""
	'The World On The Other Side…'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None

	tagmap = [
		('Drop!! ~A Tale of the Fragrance Princess~',       'Drop!! ~A Tale of the Fragrance Princess~',                      'translated'),
		('I\'ll Live My Second Life!',                      'I\'ll Live My Second Life!',                                     'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('Second Life! Chapter',                      'I\'ll Live My Second Life!',                                     'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False