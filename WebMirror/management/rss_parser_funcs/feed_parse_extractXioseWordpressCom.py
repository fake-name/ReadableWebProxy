def extractXioseWordpressCom(item):
	'''
	Parser for 'xiose.wordpress.com'
	'''

	title_concat = item['title'] + " " + " ".join(item['tags'])
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(title_concat)
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Maou Army\'s Strongest Magician was a Human',                                                'The Maou Army\'s Strongest Magician was a Human',                                                                'translated'),
		('A Dragon in Slime’s Clothing ~ I Want to Live Peacefully by Pretending to Be the Weakest',       'A Dragon in Slime\'s Clothing ~ I Want to Live Peacefully by Pretending to Be the Weakest',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False