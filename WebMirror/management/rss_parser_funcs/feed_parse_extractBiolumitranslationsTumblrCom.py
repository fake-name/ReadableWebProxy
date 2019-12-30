def extractBiolumitranslationsTumblrCom(item):
	'''
	Parser for 'biolumitranslations.tumblr.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Devil\'s Origin',       'The Devil\'s Origin',                      'translated'),
		('The Unicorn Legion',        'The Unicorn Legion',                       'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False