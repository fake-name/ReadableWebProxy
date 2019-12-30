def extractFalinmer(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	match = re.search('(\\d+)\\-(\\d+)', item['title'])
	if not vol and match:
		vol = match.group(1)
		chp = match.group(2)
	if item['title'].lower().startswith('mcm') and not 'raw' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Magi Craft Meister', vol, chp, frag=frag, postfix=postfix)
	return False
