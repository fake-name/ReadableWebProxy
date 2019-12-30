def extractFanatical(item):
	"""
	# Fanatical Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	if 'C-Drama' in item['tags']:
		return None
		
	tagmap = [
		('One Life One Incarnation Beautiful Bones', 'One Life, One Incarnation - Beautiful Bones', 'translated'),
		('Best to Have Met You',                     'Zuimei Yujian Ni',                            'translated'),
		('Blazing Sunlight',                         'Blazing Sunlight',                            'translated'),
		('Wipe Clean After Eating',                  'Chigan Mojing',                               'translated'),
		("Don't be So Proud",                        "Don't be So Proud",                           'translated'),
		('Together Forever',                         'Together Forever',                            'translated'),
		('Your Humble Servant is Guilty!',           'Your Humble Servant is Guilty!',              'translated'),
		('Stewed Squid with Honey',                  'Stewed Squid with Honey',                     'translated'),
		('Mo Bao Fei Bao',                           'Mo Bao Fei Bao',                              'translated'),
		('Hua Xu Yin',                               'Hua Xu Yin',                                  'translated'),
		('Turning Back Time',                        'Turning Back Time',                           'translated'),
		('He Yi Sheng Xiao Mo',                      'He Yi Sheng Xiao Mo',                         'translated'),
		('The Journey of Flower',                    'The Journey of Flower',                       'translated'),
		('You Are Still Here',                       'You Are Still Here',                          'translated'),
		('Come & Eat Shan Shan',                     'Come & Eat Shan Shan',                        'translated'),
		('Three Lives Three Worlds Pillow Book',     'Three Lives Three Worlds Pillow Book',        'translated'),
		('Heavy Sweetness Ash Like Frost',           'Heavy Sweetness Ash Like Frost',              'translated'),
		('You\'re My Glory',                         'You\'re My Glory',                            'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
		
		
		
	return False