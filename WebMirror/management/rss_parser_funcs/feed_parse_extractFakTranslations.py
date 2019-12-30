def extractFakTranslations(item):
	"""
	# 'Fak Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Shrouding the Heavens' in item['tags'] or 'STH' in item['tags']:
		return buildReleaseMessageWithType(item, 'Shrouding the Heavens', vol, chp, frag=frag, postfix=postfix)
	if 'KGGD' in item['tags']:
		return buildReleaseMessageWithType(item, 'Killing Grounds of Gods and Devils', vol, chp, frag=frag, postfix=postfix)
	return False
