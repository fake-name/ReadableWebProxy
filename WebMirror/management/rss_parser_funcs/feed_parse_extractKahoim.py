def extractKahoim(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Soshite Shoujo wa Akujo no Karada o Te ni Ireru' in item['tags']:
		return buildReleaseMessageWithType(item, 'Soshite Shoujo wa Akujo no Karada o Te ni Ireru', vol, chp, frag=frag, postfix=postfix)
	return False
