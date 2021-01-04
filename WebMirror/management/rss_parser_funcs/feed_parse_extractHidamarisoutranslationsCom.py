def extractHidamarisoutranslationsCom(item):
	'''
	Parser for 'hidamarisoutranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('devil wife',       'I Summoned the Devil to Grant Me a Wish, but I Married Her Instead Since She Was Adorable ~My New Devil Wife~',                      'translated'),
		('futago no ane',       'My Twin Sister Was Taken as a Miko and I Was Thrown Away but I’m Probably the Miko ',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False