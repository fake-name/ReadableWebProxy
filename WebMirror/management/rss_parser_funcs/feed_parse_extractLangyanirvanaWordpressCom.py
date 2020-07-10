def extractLangyanirvanaWordpressCom(item):
	'''
	Parser for 'langyanirvana.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['title'].startswith("Chapter ") and item['tags'] == ["Uncategorized"]:
			return buildReleaseMessageWithType(item, 'Nirvana In Fire', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		
 

	return False