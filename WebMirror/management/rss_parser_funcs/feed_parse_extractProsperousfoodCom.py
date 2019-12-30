def extractProsperousfoodCom(item):
	'''
	Parser for 'prosperousfood.com'
	'''
	if 'recipe' in item['tags']:
		return None
	if 'Movies' in item['tags']:
		return None
		
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Daddy\'s Fantasy World Restaurant',       'Daddy\'s Fantasy World Restaurant',                      'translated'),
		('Reborn - Super Chef',                     'Reborn - Super Chef',                                    'translated'),
		('Okonomiyaki Chain Store',                 'Okonomiyaki Chain Store',                                'translated'),
		('Imperial Chef Rookie',                    'Imperial Chef Rookie',                                   'translated'),
		('Kitchen Xiuzhen',                         'Kitchen Xiuzhen',                                        'translated'),
		('Here Comes The Lady Chef!',               'Here Comes The Lady Chef!',                              'translated'), 
		('Strange World Little Cooking Saint',      'Strange World Little Cooking Saint',                     'translated'), 
		('The Fine Food Broadcaster',               'The Fine Food Broadcaster',                              'translated'), 
		('Strange World Alchemist Chef',            'Strange World Alchemist Chef',                           'translated'), 
		('The Lady Chef Anecdote',                  'The Lady Chef Anecdote',                                 'translated'), 
		('The Taming of a Black Bellied Scholar',   'The Taming of a Black Bellied Scholar',                  'translated'), 
		('The Feast',                               'The Feast',                                              'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False