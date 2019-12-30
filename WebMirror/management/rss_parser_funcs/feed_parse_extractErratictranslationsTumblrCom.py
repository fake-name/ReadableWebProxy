def extractErratictranslationsTumblrCom(item):
	'''
	Parser for 'erratictranslations.tumblr.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if "Space Rebirth" in item['tags']:
		return buildReleaseMessageWithType(item, "Space Rebirth", vol, chp, frag=frag, postfix=postfix)

	return False