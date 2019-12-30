def extractNohohon(item):
	"""
	# 'Nohohon Translation'

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Monster Musume Harem wo Tsukurou!' in item['tags']:
		return buildReleaseMessageWithType(item, 'Monster Musume Harem o Tsukurou!', vol, chp, frag=frag, postfix=postfix)
	return False
