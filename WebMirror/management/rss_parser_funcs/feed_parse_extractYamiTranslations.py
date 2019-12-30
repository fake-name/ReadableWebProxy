def extractYamiTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Tensei Shoujo no Rirekisho' in item['tags']:
		return buildReleaseMessageWithType(item, 'Tensei Shoujo no Rirekisho', vol, chp, frag=frag, postfix=postfix)
	if 'shoujo resume' in item['tags']:
		return buildReleaseMessageWithType(item, 'Tensei Shoujo no Rirekisho', vol, chp, frag=frag, postfix=postfix)
	if 'Ouroboros Record' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ouroboros Record', vol, chp, frag=frag, postfix=postfix)
	if 'Light Beyond' in item['tags']:
		return buildReleaseMessageWithType(item, 'Light Beyond', vol, chp, frag=frag, postfix=postfix)
	if 'otome game ga rokkushume' in item['tags']:
		return buildReleaseMessageWithType(item, 'Otome Game Rokkushuume, Automode ga Kiremashita', vol, chp, frag=frag, postfix=postfix)
	return False