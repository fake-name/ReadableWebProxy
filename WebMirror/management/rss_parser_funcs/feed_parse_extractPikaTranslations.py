def extractPikaTranslations(item):
	"""
	# Pika Translations

	"""
	chp, vol = extractChapterVol(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Close Combat Mage' in item['tags'] or 'CCM Chapter' in item['title'] or 'Close Combat Mage Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Close Combat Mage', vol, chp)
	if 'IoR Book' in item['title'] or 'IoR B' in item['title'] or 'Inch of Radiance Book' in item['title'] or 'Inch of Radiance Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Inch of Radiance', vol, chp)
	if 'World of Immortals Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'World of Immortals', vol, chp)
	if 'Perfect World Chapter' in item['title'] or 'PW Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Perfect World', vol, chp)
	return False
