def extractEnsigsWritings(item):
	"""
	#'Ensig's Writings'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Sword-shisho' in item['tags']:
		return buildReleaseMessageWithType(item, 'I was a Sword when I Reincarnated!', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Gentle Demon' in item['tags']:
		return buildReleaseMessageWithType(item, 'Demon Noble Girl ~Tale of a Gentle Demon~', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Undead(?) Life' in item['tags']:
		return buildReleaseMessageWithType(item, 'Life(?) as an Undead', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
