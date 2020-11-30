def extractSecondlifetranslationsCom(item):
	'''
	Parser for 'secondlifetranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('IH',                                           'Immoral Holidays',                            'translated'),
		('ebpw',                                         'Everyday, Boss Is Pretending To Be Weak',     'translated'),
		('everyday, boss is pretending to be weak',      'Everyday, Boss Is Pretending To Be Weak',     'translated'),
		('icd',                                          'Indulging in Carnal Desire',                  'translated'),
		('pcpm',                                         'Please Continue Protecting Me',               'translated'),
		('please continue protecting me',                'Please Continue Protecting Me',               'translated'),
		('indulging in carnal desire',                   'Indulging in Carnal Desire',                  'translated'),
		('kisses make me grow taller',                   'kisses make me grow taller',                  'translated'),
		('wealthy supporting actress tore the script',   'Wealthy Supporting Actress Tore the Script',                      'translated'),
		('seduced by a married teacher',                 'Seduced By a Married Teacher',                      'translated'),
		('hell app',       'Hell App',                      'translated'),
		('after being turned into a dog, i conned my way into freeloading at my rival’s place',       'After Being Turned Into a Dog, I Conned My Way Into Freeloading At My Rival’s Place',                      'translated'),
		('mother of a villainess',       'Mother of a Villainess',                      'translated'),
		('erotic fairy tales',       'Erotic Fairy Tales',                      'translated'),
		('dying in the male lead’s arms every time i transmigrate',       'Dying in the Male Lead’s Arms Every Time I Transmigrate',                      'translated'),
		('being papa’d every time i transmigrate',       'Being PAPA’d Every Time I Transmigrate',                      'translated'),
		('the guide to capturing a black lotus',       'the guide to capturing a black lotus',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False