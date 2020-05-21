def extractSnowynotesHomeBlog(item):
	'''
	Parser for 'snowynotes.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == ['MTL-Novels']:

		titlemap = [
			('完美关系 羲和清零',  'The Perfect Relationship',      'translated'),
			('助理建筑师',         'Assistant Architect',           'translated'),
		]
	
		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False