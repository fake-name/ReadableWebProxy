def extractAnotherWorldTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Depths of Labyrinth' in item['tags']:
		return buildReleaseMessageWithType(item, "Aim for the Deepest Part of the Different World's Labyrinth", vol, chp, frag=frag, postfix=postfix)
	if 'Because, Janitor-san Is Not a Hero' in item['tags']:
		return buildReleaseMessageWithType(item, 'Because, Janitor-san Is Not a Hero', vol, chp, frag=frag, postfix=postfix)
	if 'World Death Game' in item['tags']:
		return buildReleaseMessageWithType(item, 'The World is Fun as it has Become a Death Game', vol, chp, frag=frag, postfix=postfix)
	return False
