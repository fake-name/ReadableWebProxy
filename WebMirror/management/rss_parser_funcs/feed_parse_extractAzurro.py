def extractAzurro(item):
	"""

	"""
	
	if not 'translation project' in item['tags']:
		return None
	if not 'review' in item['tags']:
		return None
	if 'preview' in item['title'].lower():
		return None
		
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol):
		return None
		
	if 'A Naive Short-tempered Girl' in item['tags']:
		return buildReleaseMessageWithType(item, 'A Naive Short-tempered Girl', vol, chp, frag=frag, postfix=postfix)
	if 'Substitute Bride' in item['tags']:
		return buildReleaseMessageWithType(item, 'Substitute Bride', vol, chp, frag=frag, postfix=postfix)
	if 'Husband is Great Black Belly (老公是腹黑大人)' in item['tags']:
		return buildReleaseMessageWithType(item, 'Husband is Great Black Belly', vol, chp, frag=frag, postfix=postfix)
	if "The CEO's Pregnant Wife (总裁的孕妻)" in item['tags']:
		return buildReleaseMessageWithType(item, "The CEO's Pregnant Wife", vol, chp, frag=frag, postfix=postfix)
	if 'The Wolf Husband and The Green Plum Wife (狼竹马与青梅妻)' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Wolf Husband and The Green Plum Wife', vol, chp, frag=frag, postfix=postfix)
	return False