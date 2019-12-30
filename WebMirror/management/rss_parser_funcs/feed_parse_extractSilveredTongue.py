def extractSilveredTongue(item):
	'''
	Parser for 'Silvered Tongue'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	if 'Sneak-Peek' in item['tags']:
		return None

	tagmap = [
		('Hidan no Aria',       'Hidan no Aria', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False