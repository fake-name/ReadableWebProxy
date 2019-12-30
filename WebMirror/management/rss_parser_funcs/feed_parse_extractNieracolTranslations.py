def extractNieracolTranslations(item):
	"""
	'Nieracol Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if "The Sly Emperor's Wild Beast-Tamer Empress" in item['tags']:
		return buildReleaseMessageWithType(item, "The Sly Emperor's Wild Beast-Tamer Empress", vol, chp, frag=frag, postfix=postfix)
	if 'World of Hidden Phoenixes' in item['tags']:
		return buildReleaseMessageWithType(item, 'World of Hidden Phoenixes', vol, chp, frag=frag, postfix=postfix)
	return False
