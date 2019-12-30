def extractAllaboutmynothingsBlogspotCom(item):
	'''
	Parser for 'allaboutmynothings.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Yasashii Shinjitsu to Seiryaku Kekkon',       'Yasashii Shinjitsu to Seiryaku Kekkon',                                     'translated'), 
		('Cinderella Dropped Her Panties',              'Cinderella Dropped Her Panties',                                            'translated'), 
		('Please Be More Serious',                      'Please Be More Serious',                                                    'translated'), 
		('This Has Become Serious',                     'This Has Become Serious',                                                   'translated'), 
		('Being swayed by the Deluded Shacho',          'Being swayed by the Deluded Shacho',                                        'translated'), 
		('Woman Hating Duke',                           'Women-Hating Duke Feels Lust Only For One Aristocrat Lady',                 'translated'), 
		('True and False Young Master',                 'True and False Young Master',                                               'translated'), 
		('The Love Potion',                             'The Love Potion',                                                           'translated'), 
		('Bunny Husband',                               'Bunny Husband',                                                             'translated'), 
		('Dark Empress',                                'Dark Empress',                                                              'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False