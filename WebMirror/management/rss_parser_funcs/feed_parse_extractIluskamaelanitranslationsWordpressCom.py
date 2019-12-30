def extractIluskamaelanitranslationsWordpressCom(item):
	'''
	Parser for 'iluskamaelanitranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('RSMLP',       '(Quick Transmigration) Rescuing Supporting Male Leads Plan',                      'translated'),
		('TDM',         'The Downs Of Marriage',                                                           'translated'),
		('TGCMM',       '(Transmigrated) The Girl Who Cured the Crazy BOSS is Majestic and Mighty',        'translated'),
		('BBWDE',       'Bao Bao Won’t Die Easily ',                                                       'translated'),
		('XDTH',        'Xiebing Defies The Heavens',                                                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False