def extractSaiakuTranslationsBlog(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('She Professed Herself The Pupil Of The Wiseman'):
		return buildReleaseMessageWithType(item, 'Kenja no Deshi wo Nanoru Kenja', vol, chp, frag=frag, postfix=postfix)
	return False
