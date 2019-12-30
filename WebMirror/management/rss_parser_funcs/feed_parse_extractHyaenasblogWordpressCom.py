def extractHyaenasblogWordpressCom(item):
	'''
	Parser for 'hyaenasblog.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('She was both called God, as well as Satan',       'She was both called God, as well as Satan',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	if item['title'].startswith("Chapter ") and item['tags'] == ['Uncategorized']:
			return buildReleaseMessageWithType(item, 'She was both called God, as well as Satan', vol, chp, frag=frag, postfix=postfix, tl_type='translated')

	return False