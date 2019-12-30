def extractTranslatingSloth(item):
	"""
	'Translating Sloth'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('娘子我才是娃的爹',                    'Wife, I Am the Baby\'s Father', 'translated'),
		('Wife, I Am the Baby\'s Father',       'Wife, I Am the Baby\'s Father', 'translated'),
		('I want to eat meat Wife',             'I want to eat meat Wife',       'translated'),
		('My Lord is a Stone',                  'My Lord is a Stone',            'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False