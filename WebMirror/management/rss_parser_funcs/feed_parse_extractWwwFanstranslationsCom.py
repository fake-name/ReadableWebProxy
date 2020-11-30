def extractWwwFanstranslationsCom(item):
	'''
	Parser for 'www.fanstranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('i help the richest man spend money to prevent disasters',       'i help the richest man spend money to prevent disasters',                      'translated'),
		('the widow "misses" her villainous late husband',                'the widow "misses" her villainous late husband',                               'translated'),
		('endless plunder in high school dxd',                            'endless plunder in high school dxd',                                           'translated'),
		('the legitimate daughter doesn\'t care!',                        'the legitimate daughter doesn\'t care!',                                       'translated'),
		('don\'t leave! i will lose weight for you!',                     'don\'t leave! i will lose weight for you!',                                    'translated'),
		('honeyed marriage',                                              'honeyed marriage',                                                             'translated'),
		('villainess wants to turn over a new leaf',                      'villainess wants to turn over a new leaf',                                     'translated'),
		('the rich woman is no longer acting',                            'the rich woman is no longer acting',                                           'translated'),
		('Only with Your Heart',                                          'Only with Your Heart',                                                         'translated'),
		('it’s over! the major general is bent!',                         'it’s over! the major general is bent!',                                        'translated'),
		('rich parents and hot shot brother found me at last',            'rich parents and hot shot brother found me at last',                           'translated'),
		('transmigrating as a mary sue character',                        'transmigrating as a mary sue character',                                       'translated'),
		('fortunately, you like me too',                                  'fortunately, you like me too',                                                 'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False