def extractAlyschuCo(item):
	"""
	# Alyschu & Co

	"""
	if 'PREVIEW' in item['title'] or 'preview' in item['title']:
		return False
	chp, vol = extractChapterVol(item['title'])
	if 'Against the Gods' in item['tags'] or 'Ni Tian Xie Shen (Against the Gods)' in item['title']:
		return buildReleaseMessageWithType(item, 'Against the Gods', vol, chp)
	elif 'The Simple Life of Killing Demons' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Simple Life of Killing Demons', vol, chp)
	elif 'Magic, Mechanics, Shuraba' in item['title']:
		return buildReleaseMessageWithType(item, 'Magic, Mechanics, Shuraba', vol, chp)
	elif 'The Flower Offering' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Flower Offering', vol, chp)
	return False
