def extractLittleShanksTranslations(item):
	"""
	# 'LittleShanks Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Rebirth Thief' in item['tags']:
		return buildReleaseMessageWithType(item, 'Rebirth of the Thief Who Roamed The World', vol, chp, frag=frag, postfix=postfix)
	return False
