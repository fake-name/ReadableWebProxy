def extractProfessionalGameThrowersTranslations(item):
	"""
	ProfessionalGameThrower's Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Monster Factory' in item['tags']:
		return buildReleaseMessageWithType(item, 'Monster Factory', vol, chp, frag=frag, postfix=postfix)
	if re.match('^Chapters? [\\d\\- &]+$', item['title'], re.IGNORECASE):
		return buildReleaseMessageWithType(item, 'My Ranch', vol, chp, frag=frag, postfix=postfix)
	return False
