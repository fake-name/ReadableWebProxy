def extractPyontranslationsCom(item):
	'''
	Parser for 'pyontranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	urlfrag = [
		('/i-never-run-out-of-mana-chapter',  'I Never Run Out of Mana',     'translated'),
	]

	for key, name, tl_type in urlfrag:
		if key in item['linkUrl'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False