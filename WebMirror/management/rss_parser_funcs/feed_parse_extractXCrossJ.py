def extractXCrossJ(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Character Analysis' in item['title']:
		return False
	if 'Cross Gun' in item['tags']:
		return buildReleaseMessageWithType(item, 'Cross Gun', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Konjiki no Moji Tsukai' in item['title']:
		postfix = item['title'].split(':', 1)[-1].strip()
		return buildReleaseMessageWithType(item, 'Konjiki no Wordmaster', vol, chp, frag=frag, postfix=postfix)
	if 'Shinwa Densetsu no Eiyuu no Isekaitan' in item['tags']:
		return buildReleaseMessageWithType(item, 'Shinwa Densetsu no Eiyuu no Isekaitan', vol, chp, frag=frag, postfix=postfix)
	if 'Isekai Mahou wa Okureteru' in item['tags']:
		return buildReleaseMessageWithType(item, 'Isekai Mahou wa Okureteru', vol, chp, frag=frag, postfix=postfix)
	if 'Nidome no Jinsei wo Isekai de' in item['tags']:
		return buildReleaseMessageWithType(item, 'Nidome no Jinsei wo Isekai de', vol, chp, frag=frag, postfix=postfix)
	return False
