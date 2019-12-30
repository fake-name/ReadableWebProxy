def extractIncarneous(item):
	"""
	Incarneous
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('RFSH',                                      'Raising a Fox Spirit in My Home',                      'translated'),
		('Raising a Fox Spirit in My Home',           'Raising a Fox Spirit in My Home',                      'translated'), 
		('History\'s Strongest Senior Brother',       'History\'s Strongest Senior Brother',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('RFSH Chapter',                                  'Raising a Fox Spirit in My Home',                      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if item['title'].lower().startswith(titlecomponent.lower()):
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False