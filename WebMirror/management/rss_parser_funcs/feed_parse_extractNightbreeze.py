def extractNightbreeze(item):
	"""
	# Nightbreeze Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	releases = ['Transcending The Nine Heavens', 'Stellar Transformation', 'Stellar Transformations']
	for release in releases:
		if release in item['tags']:
			return buildReleaseMessageWithType(item, release, vol, chp, frag=frag, postfix=postfix)
	return False
