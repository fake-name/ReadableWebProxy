def extractLiliesareflowersBlogspotCom(item):
	'''
	Parser for 'liliesareflowers.blogspot.com'
	'''
	
	if 'Case' in item['title'] and 'Chapter' in item['title'] and 'sci mystery files' in item['tags']:
		item['title'] = item['title'].replace("Case", "Volume")

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('reijou wa mattari wo goshomou',       'reijou wa mattari wo goshomou',                      'translated'),
		('watashi no shiawase na kekkon',       'watashi no shiawase na kekkon',                      'translated'),
		('sci mystery files',                   'sci mystery files',                                  'translated'),
		('kuraki kyuuden no shisha no ou',      'kuraki kyuuden no shisha no ou',                     'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False