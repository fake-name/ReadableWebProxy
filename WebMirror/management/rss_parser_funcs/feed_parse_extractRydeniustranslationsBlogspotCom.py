def extractRydeniustranslationsBlogspotCom(item):
	'''
	Parser for 'rydeniustranslations.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	urlfrag = [
		('/vrmmo-summoner-hajimemashita-chapter-',  'VRMMO Summoner Hajimemashita',     'translated'),
		('/maria-sama-ga-miteru-volume-',           'Maria-sama ga Miteru',             'translated'),

	]

	for key, name, tl_type in urlfrag:
		if key in item['linkUrl'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False