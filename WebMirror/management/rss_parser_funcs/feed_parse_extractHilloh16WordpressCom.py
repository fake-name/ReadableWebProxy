def extractHilloh16WordpressCom(item):
	'''
	Parser for 'hilloh16.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	if item['tags'] == ['Uncategorized']:
		chp_prefixes = [
				('The Ugly Empress',  'The Ugly Empress',               'translated'),
			]
	
		for prefix, series, tl_type in chp_prefixes:
			if item['title'].lower().startswith(prefix.lower()):
				return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	
	return False