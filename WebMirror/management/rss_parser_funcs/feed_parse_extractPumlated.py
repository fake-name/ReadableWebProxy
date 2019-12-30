def extractPumlated(item):
	"""
	Pumlated
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower() or 'incomplete' in item['title'].lower():
		return None
	if "(Um, Sorry!) I've been Reincarnated!" in item['tags']:
		return buildReleaseMessageWithType(item, "(Um, Sorry!) I've been Reincarnated!", vol, chp, frag=frag, postfix=postfix)
		
		
	tagmap = [
		('(Um, Sorry!) I\'ve been Reincarnated!',       '(Um, Sorry!) I\'ve been Reincarnated!',                      'translated'),
		('The Counterfeit Madam Hou',                   'The Counterfeit Madam Hou',                                  'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False