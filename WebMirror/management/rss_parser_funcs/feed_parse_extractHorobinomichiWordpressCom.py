def extractHorobinomichiWordpressCom(item):
	'''
	Parser for 'horobinomichi.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('weisselillie',       'Weisselillie ~senka ni sasagu ai no hana, soredemo atashi wa sekai ga hoshii~',    'translated'),
		('maid in isekai',     'Maid in Isekai ≪Fantasia≫',                                                       'translated'),
		('autodoll',           'Autodoll wa Kuchita Sekai de Yume wo Miru',                                        'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False