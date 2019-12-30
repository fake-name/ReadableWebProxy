def extractImoutositeWordpressCom(item):
	'''
	Parser for 'imoutosite.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
	if ' Manga ' in item['title']:
		return None
		
	ltitle = item['title'].lower()
		
	chp_prefixes = [
			("chapter ",                       "The Reincarnated Vampire Wants an Afternoon Nap",                  False),
			("arge chapter ",                  "The Reincarnated Vampire Wants an Afternoon Nap",                  False),
			("arge chaper ",                   "The Reincarnated Vampire Wants an Afternoon Nap",                  False),

			("mile ",                          "I Said Make My Abilities Average!",                                False),
			("kazane chapter",                 "Manowa Mamono Taosu Nouryoku Ubau Watashi Tsuyokunaru",            False),
			("mira ",                          "She Professed Herself The Pupil Of The Wiseman",                   False),
			("cathy chapter",                  "Sword Saint\'s Disciple",                                          False),
			("asley chapter",                  'The Principle of a Philosopher by eternal fool "Asley"',           False),
			("kaoru's chapter ",               'Average Potion Maker Goddess',                                     False),
			("kaoru chapter ",                 'Average Potion Maker Goddess',                                     False),
			("kaoru chaper ",                  'Average Potion Maker Goddess',                                     False),
			("mitsuha ",                       'Saving 80,000 Gold in an Another World for Retirement',            False),
			("taru chapter ",                'Even I have become a beautiful girl, but I was just spending my time playing as a Net-Game addict',            False),
		]

	for titlefrag, series, require_chp in chp_prefixes:
		if ltitle.startswith(titlefrag) and (not require_chp or 'chapter' in ltitle.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix)

	urlfrag = [
		('/potion-maker-chapter-',                  'Average Potion Maker Goddess',     'translated'),
		('/average-potion-maker-goddess-chapter-',  'Average Potion Maker Goddess',     'translated'),
		('/potion-maker-goddess-average-chapter-',  'Average Potion Maker Goddess',     'translated'),
	]

	for key, name, tl_type in urlfrag:
		if key in item['linkUrl'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	
	
	return False