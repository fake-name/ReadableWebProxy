def extractSnowyPublications(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'New Release: ' in item['title']:
		return buildReleaseMessageWithType(item, 'Whisper of the Nightingale', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'WN' in item['tags']:
		return buildReleaseMessageWithType(item, 'Whisper of the Nightingale', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'DD' in item['tags']:
		return buildReleaseMessageWithType(item, 'Dimension’s Door', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
