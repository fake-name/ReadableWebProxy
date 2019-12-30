def extract愛主の翻訳AinushiTranslations(item):
	"""
	'愛主の翻訳  Ainushi Translations'
	"""
	if 'Oneshots' in item['tags']:
		return None
	if 'Manhua' in item['tags']:
		return None
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
		
	tagmap = [
		('The prince has all kinds of strange hobbies',                      'The prince has all kinds of strange hobbies',                                'translated'),
		('Masculine Puppy',                                                  'Masculine Puppy',                                                            'translated'),
		('Waiting Upon You',                                                 'Waiting Upon You',                                                           'translated'),
		('Stop Bothering Me, Emperor',                                       'Stop Bothering Me, Emperor',                                                 'translated'),
		('Midnight Cinderella',                                              'Midnight Cinderella',                                                        'translated'),
		('Silent Reading',                                                   'Silent Reading',                                                             'translated'),
		('Qizi',                                                             'Qizi',                                                                       'translated'),
		('Open Sea',                                                         'Open Sea',                                                                   'translated'),
		('Estrus Gymnasium',                                                 'Estrus Gymnasium',                                                           'translated'),
		('Thousand Autumns',                                                 'Thousand Autumns',                                                           'translated'),
		('Broken-Winged Angel',                                              'Broken-Winged Angel',                                                        'translated'),
		('Maid Kara Haha ni Narimashita',                                    'Maid Kara Haha ni Narimashita',                                              'translated'),
		('maou no utsuwa',                                                   'Maou no Utsuwa',                                                             'translated'),
		('Ossan Idol',                                                       'Ossan (36) Ga Idol Ni Naru Hanashi',                                         'translated'),
		('Buy One Get One Free',                                             '$10 Trillion Wife, Buy One Get One Free',                                    'translated'),
		('happy life',                                                       'Tensei Shitanode Tsugi Koso wa Shiawasena Jinsei wo Tsukande Misemashou',    'translated'),
		('Monogusana Kenja',                                                 'Monogusana Kenja',                                                           'translated'),
		('Loner and Juliet',                                                 'Loner and Juliet',                                                           'translated'),
		('Great God',                                                        'Great God, I\'ll Support You',                                               'translated'),
		('Heroine Sister',                                                   'My Sister the Heroine, and I the Villainess',                                'translated'),
		('Mob',                                                              'Mob… Sore mo waki mob no hazu nan desu kedo!?',                              'translated'),
		('Re: Hero no Kaa-san',                                              'Re: Hero no Kaa-san',                                                        'translated'),
		('guardian',                                                         'Guardian',                                                                   'translated'),
		('Maou no Ki',                                                       'Maou no Ki',                                                                 'translated'),
		('True or False',                                                    'True Or False? ~ Love Game? No, I Will Not Participate In The Competition',  'translated'),
		('Crying in the Night Unseen',                                       'Crying in the Night Unseen',                                                 'translated'),
		('Flowers Reflecting The Sky',                                       'Flowers Reflecting The Sky',                                                 'translated'),
		('Debt Girl',                                                        'The Noble Girl Living in Debt',                                              'translated'),
		('The Reader and Protagonist Definitely Have to Be in True Love',    'The Reader and Protagonist Definitely Have to Be in True Love',              'translated'),
		('As the Minor Gay Love Rival in Het Novels',                        'As the Minor Gay Love Rival in Het Novels',                                  'translated'),
		('Divorce: This is a Trivial Matter',                                'Divorce: This is a Trivial Matter',                                          'translated'),
		('KtBC',                                                             'Kiss the Black Cat',                                                         'translated'),
		
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
		
		
	return False