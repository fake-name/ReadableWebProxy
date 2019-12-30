def extractAtenTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Skill Taker' in item['tags'] or 'Skill Taker Ch' in item['title']:
		return buildReleaseMessageWithType(item, 'Skill Taker’s World Domination ~ Building a Slave Harem from Scratch', vol, chp, frag=frag, postfix=postfix)
	return False
