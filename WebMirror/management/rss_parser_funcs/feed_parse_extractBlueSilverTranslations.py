def extractBlueSilverTranslations(item):
	"""
	# Blue Silver Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Douluo Dalu' in item['tags']:
		proc_str = '%s %s' % (item['tags'], item['title'])
		proc_str = proc_str.replace("'", ' ')
		chp, vol = extractChapterVol(proc_str)
		return buildReleaseMessageWithType(item, 'Douluo Dalu', vol, chp)
	if 'Immortal Executioner' in item['tags']:
		return buildReleaseMessageWithType(item, 'Immortal Executioner', vol, chp, frag=frag, postfix=postfix)
	if 'Stellar War Storm' in item['tags']:
		return buildReleaseMessageWithType(item, 'Stellar War Storm', vol, chp, frag=frag, postfix=postfix)
	if 'Bringing The Farm To Live In Another World' in item['tags']:
		return buildReleaseMessageWithType(item, 'Bringing The Farm To Live In Another World', vol, chp, frag=frag, postfix=postfix)
	if 'Law of the Devil' in item['tags']:
		return buildReleaseMessageWithType(item, 'Law of the Devil', vol, chp, frag=frag, postfix=postfix)
	return False