def extractOriginNovels(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if '–' in item['title']:
		postfix = item['title'].split('–')[-1]
	if 'True Identity' in item['tags']:
		return buildReleaseMessageWithType(item, 'True Identity', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
