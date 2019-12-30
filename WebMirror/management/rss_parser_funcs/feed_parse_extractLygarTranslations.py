def extractLygarTranslations(item):
	"""
	# Lygar Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if ('elf tensei' in item['tags'] or 'elf tensei' in item['title'].lower()) and not 'news' in item['tags']:
		return buildReleaseMessageWithType(item, 'Elf Tensei Kara no Cheat Kenkoku-ki', vol, chp, frag=frag, postfix=postfix)
	if 'Himekishi ga Classmate' in item['tags'] and not 'poll' in item['tags']:
		return buildReleaseMessageWithType(item, 'Himekishi ga Classmate! ~ Isekai Cheat de Dorei ka Harem~', vol, chp, frag=frag, postfix=postfix)
	return False
