def extractEbisutranslationsWordpressCom(item):
	'''
	Parser for 'ebisutranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	tagmap = [
		('Invijible Panda',                                                                'Invijible Panda',                                                                               'oel'),   # wtf?
		('I Reincarnated and Tried to Become a Genius Child Actor. I Want to Quit.',       'I Reincarnated and Tried to Become a Genius Child Actor. I Want to Quit.',                      'translated'),
		('Hey, Don\'t Act Unruly!',                                                        'Hey, Don\'t Act Unruly!',                                                                       'translated'),
		('The support manages adventurer parties',                                         'The support manages adventurer parties',                                                        'translated'),
		('My Pet Is a Holy Maiden',                                                        'My Pet Is a Holy Maiden',                                                                       'translated'),
		('I Bought a Girl',                                                                'I Bought a Girl',                                                                               'translated'),
		('I Heard You Like Me Too',                                                        'I Heard You Like Me Too',                                                                       'translated'),
		('Wife, You Can\'t Run After Eating',                                              'Wife, You Can\'t Run After Eating',                                                             'translated'),
		('Can\'t Leave This Room Until I Get First Place on Syosetu',                      'Can\'t Leave This Room Until I Get First Place on Syosetu',                                     'translated'),
		('Child Rearing Hero and Demon King\'s children',                                  'Child Rearing Hero and Demon King\'s children',                                                 'translated'),
		('How Is It My Fault That I Look Like a Girl!',                                    'How Is It My Fault That I Look Like a Girl!',                                                   'translated'),
		('Pampering Big Cat Wife',                                                         'Pampering Big Cat Wife',                                                                        'translated'),
		('Reincarnated as My Little Sister',                                               'Reincarnated as My Little Sister',                                                              'translated'),
		('Strongly Pampered Male Wife',                                                    'Strongly Pampered Male Wife',                                                                   'translated'),
		('Perfect Superstar',                                                              'Perfect Superstar',                                                                             'translated'),
		('Being An Author Is A High Risk Occupation',                                      'Being An Author Is A High Risk Occupation',                                                     'translated'),
		('Shoujo Grand Summoning',                                                         'Shoujo Grand Summoning',                                                                        'translated'),
		('The Worst Princes\' Battle Over Giving Up the Throne',                           'The Worst Princes\' Battle Over Giving Up the Throne',                                          'translated'),
		('In Search Of Love',                                                              'In Search Of Love',                                                                             'translated'),
		('Unlimited Anime Works',                                                          'Unlimited Anime Works',                                                                         'translated'),
		('Noble Reincarnation',                                                            'Noble Reincarnation~Blessed With the Strongest Power From Birth',                               'translated'),
		('Star Martial God Technique',                                                     'Star Martial God Technique',                                                                    'translated'),
		('a misunderstood mentor',                                                         'a misunderstood mentor',                                                                        'translated'),
		('Holistic Fantasy',                                                               'Holistic Fantasy',                                                                              'translated'),
		('Little Husband, Little Wife, Little Immortal',                                   'Little Husband, Little Wife, Little Immortal',                                                  'translated'),
		('Reborn as the Hero\'s Daughter! Time to Become the Hero Once More!',             'Reborn as the Hero\'s Daughter! Time to Become the Hero Once More!',                            'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('HIIMFTILLAG',                                    'How Is It My Fault That I Look Like a Girl!',                                                   'translated'),
		('HDAU',                                           'Hey, Don\'t Act Unruly!',                                                                       'translated'),
		('TSOUG',                                          'The School\'s Omnipotent Useless Garbage',                                                      'translated'),
		('IBAG',                                           'I Bought a Girl',                                                                               'translated'),
		('SMAP',                                           'The support manages adventurer parties',                                                        'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent in item['title']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False