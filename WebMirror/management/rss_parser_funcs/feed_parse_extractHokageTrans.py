def extractHokageTrans(item):
	"""
	# Hokage Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if any([('Aim the Deepest Part of the Different World Labyrinth'.lower() in tag.lower()) for tag in item['tags']]):
		if re.match('\\d+\\.', item['title']):
			postfix = item['title'].split('.', 1)[-1]
		return buildReleaseMessageWithType(item, 'Aim the Deepest Part of the Different World Labyrinth', vol, chp, frag=frag, postfix=postfix)
	if any([('Divine Protection of Many Gods'.lower() in tag.lower()) for tag in item['tags'] + [item['title']]]):
		return buildReleaseMessageWithType(item, 'Divine Protection of Many Gods', vol, chp, frag=frag, postfix=postfix)
	if any([('Because Janitor-san is Not a Hero'.lower() in tag.lower()) for tag in item['tags'] + [item['title']]]):
		return buildReleaseMessageWithType(item, 'Because Janitor-san is Not a Hero', vol, chp, frag=frag, postfix=postfix)
	return False
