def extractYorasuTranslations(item):
	"""
	# Yoraikun
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('DKFTOD'):
		return buildReleaseMessageWithType(item, 'Devil King From The Otherworldly Dimension', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Hacker'):
		return buildReleaseMessageWithType(item, 'Hacker', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Fallen God Records'):
		return buildReleaseMessageWithType(item, 'Fallen God Records', vol, chp, frag=frag, postfix=postfix)
	if 'Godly Model Creator' in item['tags']:
		return buildReleaseMessageWithType(item, 'Godly Model Creator', vol, chp, frag=frag, postfix=postfix)
	if 'Super Brain Telekinesis' in item['tags']:
		return buildReleaseMessageWithType(item, 'Super Brain Telekinesis', vol, chp, frag=frag, postfix=postfix)
	if 'Super soldier' in item['tags']:
		return buildReleaseMessageWithType(item, 'Super soldier', vol, chp, frag=frag, postfix=postfix)
	if 'The Different World Of Demon Lord' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Different World Of Demon Lord', vol, chp, frag=frag, postfix=postfix)
	return False
