def extractKuukaiWeeblyCom(item):
	'''
	Parser for 'kuukai.weebly.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Zannen Oujo',       'Zannen Kei na Ojou-sama no Nichijou',                      'translated'), 
		('Shiro Buta',        'Tensei Saki ga Shoujo Manga no Shiro Buta Reijou datta',   'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False