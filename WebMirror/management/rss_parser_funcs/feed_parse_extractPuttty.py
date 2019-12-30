def extractPuttty(item):
	"""
	# putttytranslations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if any([('god of thunder' == val.lower()) for val in item['tags']]) and (vol or chp):
		if ':' in item['title']:
			postfix = item['title'].split(':', 1)[-1]
		return buildReleaseMessageWithType(item, 'God of Thunder', vol, chp, frag=frag, postfix=postfix)
	if 'Beseech the devil'.lower() in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Beseech the Devil', vol, chp, frag=frag, postfix=postfix)
	if 'Goblin' in item['tags']:
		return buildReleaseMessageWithType(item, 'Goblin', vol, chp, frag=frag, postfix=postfix)
	if 'King of the Eternal Night' in item['tags']:
		return buildReleaseMessageWithType(item, 'King of the Eternal Night', vol, chp, frag=frag, postfix=postfix)
	if 'Martial World' in item['tags']:
		return buildReleaseMessageWithType(item, 'Martial World', vol, chp, frag=frag, postfix=postfix)
	return False
