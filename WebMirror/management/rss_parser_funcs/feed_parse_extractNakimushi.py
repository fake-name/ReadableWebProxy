def extractNakimushi(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Teasers' in item['tags']:
		return None
		
	if 'Renai Kakumei Onii-chan' in item['tags']:
		return buildReleaseMessageWithType(item, 'I, am Playing the Role of the Older Brother in Heart-throb Love Revolution.', vol, chp, frag=frag, postfix=postfix)
	if 'Takamura-kun is Cursed.' in item['tags']:
		return buildReleaseMessageWithType(item, 'Takamura-kun is Cursed', vol, chp, frag=frag, postfix=postfix)
	if 'Escape Galge Protagonist' in item['tags']:
		return buildReleaseMessageWithType(item, 'As a Capturable Character I Want to Escape from Galge Protagonist!', vol, chp, frag=frag, postfix=postfix)
	if 'Role of (Villain/Heroine)' in item['tags']:
		return buildReleaseMessageWithType(item, 'I Play the Role of (Villain/Heroine) in a Japanese-style Otome Game', vol, chp, frag=frag, postfix=postfix)
		
	return False