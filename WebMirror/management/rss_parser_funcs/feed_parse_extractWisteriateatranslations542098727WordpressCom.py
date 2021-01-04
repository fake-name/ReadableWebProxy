def extractWisteriateatranslations542098727WordpressCom(item):
	'''
	Parser for 'wisteriateatranslations542098727.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('i\'m a d-rank adventurer, for some reason i got recruited into a hero party, and now the princess is stalking me.',       'i\'m a d-rank adventurer, for some reason i got recruited into a hero party, and now the princess is stalking me.',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False