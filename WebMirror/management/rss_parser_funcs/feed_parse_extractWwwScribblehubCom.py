def extractWwwScribblehubCom(item):
	'''
	Parser for 'www.scribblehub.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if len(item['tags']) == 2:
		item_title, item_id = item['tags']
		if item_id.isdigit():
			return buildReleaseMessageWithType(item, item_title, vol, chp, frag=frag, postfix=postfix, tl_type="oel")
		item_id, item_title = item['tags']
		if item_id.isdigit():
			return buildReleaseMessageWithType(item, item_title, vol, chp, frag=frag, postfix=postfix, tl_type="oel")
			

	return False