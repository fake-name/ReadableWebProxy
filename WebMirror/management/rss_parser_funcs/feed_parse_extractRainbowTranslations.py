def extractRainbowTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Myriad of Shades' in item['tags']:
		return buildReleaseMessageWithType(item, 'Myriad of Shades', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
