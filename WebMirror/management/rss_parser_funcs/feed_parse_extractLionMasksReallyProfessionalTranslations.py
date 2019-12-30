def extractLionMasksReallyProfessionalTranslations(item):
	"""
	Lion Mask's Really Professional Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	if 'slime-translation' in item['tags']:
		return buildReleaseMessageWithType(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)
	
	if item['title'].lower().startswith('shaman chapter '):
		return buildReleaseMessageWithType(item, 'The Shaman can\'t become a Hero', vol, chp, frag=frag, postfix=postfix)
		
	
	return False