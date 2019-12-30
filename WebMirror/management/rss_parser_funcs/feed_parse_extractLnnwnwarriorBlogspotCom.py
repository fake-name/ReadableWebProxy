def extractLnnwnwarriorBlogspotCom(item):
	'''
	Parser for 'lnnwnwarrior.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	chp_prefixes = [
			('LBADDWSB Chapter ',  'Let\'s be an Adventurer! ~Defeating Dungeons with a Skill Board~',               'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False