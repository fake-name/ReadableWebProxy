def extractCircleofShards(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	print(item['title'])
	print(item['tags'])
	print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))
	if re.match('^Chapter \\d+', item['title'], re.IGNORECASE):
		return buildReleaseMessageWithType(item, 'Circle of Shards', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
