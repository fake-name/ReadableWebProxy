def extractWwwLaundrybasketXyz(item):
	'''
	Parser for 'www.laundrybasket.xyz'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	urlfrag = [
		('https://www.laundrybasket.xyz/i-became-the-secretary-of-a-tyrant/chapter-',  'I Became the Secretary of a Tyrant',     'translated'),
		('https://www.laundrybasket.xyz/an-evil-cinderella-needs-a-villain/chapter-',  'An Evil Cinderella Needs a Villain',     'translated'),

		('rebirth.online/novel/earths-core' ,          "Earth's Core", 'oel'),
	]

	for key, name, tl_type in urlfrag:
		if key in item['linkUrl'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False