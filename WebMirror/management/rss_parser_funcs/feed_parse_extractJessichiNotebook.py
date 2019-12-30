def extractJessichiNotebook(item):
	'''
	Parser for 'Jessichi Notebook'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if 'PS Vita' in item['tags']:
		return None

	tagmap = [
		('outaishihi ni nante naritakunai',       'Outaishihi ni Nante Naritakunai!!',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False