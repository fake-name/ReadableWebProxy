def extractSinisterTranslations(item):
	"""
	Sinister Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Goblin Slayer' in item['tags']:
		return buildReleaseMessageWithType(item, 'Goblin Slayer', vol, chp, frag=frag, postfix=postfix)
	if 'Daily Life of an Immortal Cat in the Human World' in item['tags']:
		return buildReleaseMessageWithType(item, 'Daily Life of an Immortal Cat in the Human World', vol, chp, frag=frag, postfix=postfix)
	if 'Death Notice' in item['tags']:
		return buildReleaseMessageWithType(item, 'Death Notice', vol, chp, frag=frag, postfix=postfix)
	if 'Hollywood Secret Garden' in item['tags']:
		return buildReleaseMessageWithType(item, 'Hollywood Secret Garden', vol, chp, frag=frag, postfix=postfix)
	if 'Strange Life of a Cat' in item['tags']:
		return buildReleaseMessageWithType(item, 'Strange Life of a Cat', vol, chp, frag=frag, postfix=postfix)
	if "The Path of the Cannon Folder's Counterattack" in item['tags']:
		return buildReleaseMessageWithType(item, "The Path of the Cannon Folder's Counterattack", vol, chp, frag=frag, postfix=postfix)
	return False
