def extractForsakenmoonlightWordpressCom(item):
	'''
	Parser for 'forsakenmoonlight.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == ['Uncategorized']:
		prefix = item['title'].split(" ")[0]
		try:
			int(prefix)
			
			return buildReleaseMessageWithType(item, "Reborn Spoiled Ming Wangfei", vol, chp, frag=frag, postfix=postfix, tl_type="translated")
			
		except ValueError:
			pass

	tagmap = [
		('RSMW',       'Reborn Spoiled Ming Wangfei',                                                 'translated'),
		('pddc',       'Poison Doctor Demon Consort: Xiao wang, Loving Nightly',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False