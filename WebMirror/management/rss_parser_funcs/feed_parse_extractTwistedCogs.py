def extractTwistedCogs(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if '–' in item['title']:
		postfix = item['title'].split('–', 1)[-1].strip()
	if 'smut' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Twisted Smut', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return buildReleaseMessageWithType(item, 'Twisted Cogs', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
