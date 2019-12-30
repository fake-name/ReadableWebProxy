def extractSpaceforMemory(item):
	"""
	'SpaceforMemory'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Beloved Villain' in item['tags']:
		return buildReleaseMessageWithType(item, 'Beloved Villain Flips the Skies', vol, chp, frag=frag, postfix=postfix)
	if 'Dukes Daughter' in item['tags']:
		return buildReleaseMessageWithType(item, 'Koushaku Reijou no Tashinami', vol, chp, frag=frag, postfix=postfix)
	if 'Lady Rose' in item['tags']:
		return buildReleaseMessageWithType(item, 'Lady Rose Wants to be a Commoner', vol, chp, frag=frag, postfix=postfix)
	
	
	# Jesus, really?
	if '( ´_ゝ`)' in item['tags']:
		return buildReleaseMessageWithType(item, 'I obtained a stepmother. I obtained a little brother. It appears that little brother is not father’s child, but a scum king’s child, however, don’t mind it please ( ´_ゝ`)', vol, chp, frag=frag, postfix=postfix)
	
	return False