def extractJawzPublications(item):
	"""
	'Jawz Publications'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Zectas' in item['tags'] and vol and chp:
		return buildReleaseMessageWithType(item, 'Zectas', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'LMS' in item['tags'] and vol and chp:
		return buildReleaseMessageWithType(item, 'Legendary Moonlight Sculptor', vol, chp, frag=frag, postfix=postfix)
	return False