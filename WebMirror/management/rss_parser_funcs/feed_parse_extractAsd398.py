def extractAsd398(item):
	"""
	# 'asd398'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if "Don't tell me this is the true history of the Three Kingdoms!" in item['tags']:
		return buildReleaseMessageWithType(item, "Don't tell me this is the true history of the Three Kingdoms!", vol, chp, frag=frag, postfix=postfix)
	if 'Leading an Explosive Revolution in Another World!' in item['tags']:
		return buildReleaseMessageWithType(item, 'Leading an Explosive Revolution in Another World!', vol, chp, frag=frag, postfix=postfix)
	if 'No Battle No Life' in item['tags']:
		return buildReleaseMessageWithType(item, 'No Battle No Life', vol, chp, frag=frag, postfix=postfix)
	return False
