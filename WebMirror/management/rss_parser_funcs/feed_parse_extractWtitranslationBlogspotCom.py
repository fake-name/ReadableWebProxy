def extractWtitranslationBlogspotCom(item):
	'''
	Parser for 'wtitranslation.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None


	if item['tags'] == [] and item['title'].startswith("Chapter "):
		return buildReleaseMessageWithType(item, "Womanizing True Immortal", vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		
	if item['tags'] == ['Chapters'] and item['title'].startswith("Chapter "):
		return buildReleaseMessageWithType(item, "Womanizing True Immortal", vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		
		
	return False