def extractWwwWolfiehonyakuCom(item):
	'''
	Parser for 'www.wolfiehonyaku.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The amber sword',                      'The Amber Sword',                      'translated'),
		('The latest game is too amazing',       'The Latest Game is too Amazing',       'translated'),
		('The strategy to become good at magic', 'The Strategy to Become Good at Magic', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False