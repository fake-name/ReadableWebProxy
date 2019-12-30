def extractSoupytranslationsBlogspotCom(item):
	'''
	Parser for 'soupytranslations.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Thousand Face Demonic Concubine',                                                   'Thousand Face Demonic Concubine',                                                  'translated'),
		('TFDC',                                                                              'Thousand Face Demonic Concubine',                                                  'translated'), 
		('Good for nothing alchemist: tyrant emperor dotes on small alchemist consort',       'Good for nothing alchemist: tyrant emperor dotes on small alchemist consort',      'translated'),
		('GFNA',                                                                              'Good for nothing alchemist: tyrant emperor dotes on small alchemist consort',      'translated'), 
		('Thousand Face Demonic Concubine',                                                   'Thousand Face Demonic Concubine',                                                  'translated'),
		('Lovable Beauty',                                                                    'Lovable Beauty',                                                                   'translated'), 
		('Why not soar your majesty',                                                         'Why not soar your majesty',                                                        'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False