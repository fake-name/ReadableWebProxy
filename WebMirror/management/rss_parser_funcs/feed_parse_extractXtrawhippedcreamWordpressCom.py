def extractXtrawhippedcreamWordpressCom(item):
	'''
	Parser for 'xtrawhippedcream.wordpress.com'
	'''
	if 'Manga/Manhua' in item['tags']:
		return None
		
		
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Female Emperor\'s Peerless Luck',                                            'Female Emperor\'s Peerless Luck',                                                      'translated'),
		('I Dedicated the Dimension to the Country',                                   'I Dedicated the Dimension to the Country',                                             'translated'),
		('Quick Transmigration - Villain Walkthrough',                                 'Quick Transmigration - Villain Walkthrough',                                           'translated'),
		('Considering the Possibility of Falling in Love With the Villain [GL]',       'Considering the Possibility of Falling in Love With the Villain',                      'translated'),
		('Befriending The Most Powerful Person',                                       'Befriending The Most Powerful Person',                                                      'translated'),
		('Reborn, I Became a Male God',                                                'Reborn, I Became a Male God',                                                               'translated'),
		('I am Not a Chick',                                                           'I am Not a Chick',                                                                          'translated'),
		('Living in the Last Days',                                                    'Living in the Last Days',                                                                   'translated'),
		('Love Fraudster',                                                             'Love Fraudster',                                                                            'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False