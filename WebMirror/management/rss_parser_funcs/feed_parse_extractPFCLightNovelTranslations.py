def extractPFCLightNovelTranslations(item):
	"""
	'PFC – Light Novel Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Qualidea Code: Itsuka Sekai wo Sukuu Tame ni',              'Itsuka Sekai wo Sukuu Tame ni -Qualidea Code-',               'translated'),
		('Qualidea Code: Doudemo ii Sekai Nante',                     'Doudemo ii Sekai Nante -Qualidea Code-',                      'translated'),
		('Qualidea Code: Doudemo ii Sekai Nante Vol. 2',              'Doudemo ii Sekai Nante -Qualidea Code-',                      'translated'),
	]
	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False