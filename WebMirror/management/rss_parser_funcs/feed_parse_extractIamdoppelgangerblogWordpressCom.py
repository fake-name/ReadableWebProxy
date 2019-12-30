def extractIamdoppelgangerblogWordpressCom(item):
	'''
	Parser for 'iamdoppelgangerblog.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['title'].startswith('Chapter '):
		return buildReleaseMessageWithType(item, "I Am Doppelganger", vol, chp, frag=frag, postfix=postfix)

	return False