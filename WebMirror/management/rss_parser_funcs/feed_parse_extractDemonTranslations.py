def extractDemonTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'The Gate Of Good Fortune' in item['tags'] or item['title'].startswith('New TGOGF Chapter Release!!'):
		return buildReleaseMessageWithType(item, 'The Gate Of Good Fortune', vol, chp, frag=frag, postfix=postfix)
	if 'The Unsuspecting Journey' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Unsuspecting Journey', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
