def extractAmateurtranslationsCom(item):
	'''
	Parser for 'amateurtranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Phoenix Against The World',       'Across the Stunning Beast Princess: Phoenix Against the World',   'translated'),
		('Hidden Marriage',                 'Hidden Marriage',                                                 'translated'),
		('Sonata: FAAAM',                   'Sonata: Fleeing To Avoid An Arranged Marriage',                   'translated'),
		('Princess Husband',                'Princess Husband, Too Mensao!',                                   'translated'),
		('My Chief Husband',                'My Chief Husband, Too Mensao!',                                   'translated'),
		('Level-Up Dr',                     'Level Up Doctor Choi Kiseok',                                     'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False