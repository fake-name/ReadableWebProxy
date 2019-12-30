def extractNovelcvCom(item):
	'''
	Parser for 'novelcv.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
	# Seems dead now
	return None

	tagmap = [
		# ('Isekai Tensei - Kimi to no Saikai made Nagai koto Nagai koto',                          'Isekai Tensei - Kimi to no Saikai made Nagai koto Nagai koto',                                         'translated'),
		# ('Era of Disaster',                                                                       'Era of Disaster',                                                                                      'translated'),
		# ('I&#039;ve Led the Villain Astray, How Do I Fix It?',                                    'I\'ve Led the Villain Astray, How Do I Fix It?',                                                       'translated'),
		# ('Succubus-san&#039;s Life in a Another World',                                           'Succubus-san\'s Life in a Another World',                                                              'translated'),
		# ('Anonym & Switch, Obtaining Power to Retaliate',                                         'Anonym & Switch, Obtaining Power to Retaliate',                                                        'translated'),
		# ('Illusion',                                                                              'Illusion',                                                                                             'translated'),
		# ('Parameter remote controller',                                                           'Parameter remote controller',                                                                          'translated'),
		# ('Emperor’s Domination',                                                                  'Emperor\'s Domination',                                                                                'translated'),
		# ('King of Gods',                                                                          'King of Gods',                                                                                         'translated'),
		# ('Martial God Asura',                                                                     'Martial God Asura',                                                                                    'translated'),
		# ('Dragon-Marked War God',                                                                 'Dragon-Marked War God',                                                                                'translated'),
		# ('Hidden Marriage',                                                                       'Hidden Marriage',                                                                                      'translated'),
		
		
		# ("Genius Doctor: Black Belly Miss",                                                "Genius Doctor: Black Belly Miss",                                                'translated'),
		# ("I HOPE I SHALL ARRIVE SOON",                                                     "I hope I shall arrive soon",                                                     'translated'),
		# ("Miracle Doctor, Abandoned Daughter: The Sly Emperor’s Wild Beast-Tamer Empress", "Miracle Doctor, Abandoned Daughter: The Sly Emperor’s Wild Beast-Tamer Empress", 'translated'),
		# ("Release that Witch",                                                             "Release that Witch",                                                             'translated'),
		# ("Royal Roader on My Own",                                                         "Royal Roader on My Own",                                                         'translated'),
		# ("Soaring of Galaxia",                                                             "Soaring of Galaxia",                                                             'translated'),
		# ("War Sovereign Soaring The Heavens",                                              "War Sovereign Soaring The Heavens",                                              'translated'),
		
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False