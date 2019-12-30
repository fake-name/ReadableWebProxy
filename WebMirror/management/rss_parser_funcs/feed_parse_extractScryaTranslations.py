def extractScryaTranslations(item):
	"""
	# Scrya Translations

	"""
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if "So What if It's an RPG World!?" in item['tags']:
		return buildReleaseMessageWithType(item, "So What if It's an RPG World!?", vol, chp, frag=frag)
	if 'My Disciple Died Yet Again' in item['tags']:
		return buildReleaseMessageWithType(item, 'My Disciple Died Yet Again', vol, chp, frag=frag)
	if '[Disciple] Releases' in item['tags']:
		return buildReleaseMessageWithType(item, 'My Disciple Died Yet Again', vol, chp, frag=frag)
	return False