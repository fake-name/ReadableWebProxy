def extractUselessno4(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('Skeleton Knight '):
		return buildReleaseMessageWithType(item, 'Skeleton Knight, in another world', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('1000 hugs '):
		return buildReleaseMessageWithType(item, '1000 nin no Homunkurusu no Shoujo tachi ni Kakomarete Isekai Kenkoku', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Paladin '):
		extract = re.search('(\\d+)\\-(\\d+)', item['title'], re.IGNORECASE)
		if extract and not frag:
			chp = int(extract.group(1))
			frag = int(extract.group(2))
		return buildReleaseMessageWithType(item, 'Paladin of the End', vol, chp, frag=frag, postfix=postfix)
	return False
