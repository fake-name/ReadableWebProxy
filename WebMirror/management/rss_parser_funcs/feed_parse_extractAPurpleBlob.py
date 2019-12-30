def extractAPurpleBlob(item):
	"""
	A Purple Blob
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if re.match('^Nirvana in Fire Chapter \\d+', item['title'], re.IGNORECASE):
		return buildReleaseMessageWithType(item, 'Nirvana in Fire', vol, chp, frag=frag, postfix=postfix)
	return False
