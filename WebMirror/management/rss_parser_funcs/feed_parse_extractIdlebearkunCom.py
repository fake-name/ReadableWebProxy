def extractIdlebearkunCom(item):
	'''
	Parser for 'idlebearkun.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Villain heal: The villainess’s plan to heal a broken heart',       'Villain heal: The villainess\'s plan to heal a broken heart',                      'translated'),
		('Second life: I will be the best in this second life!',             'Second life: I will be the best in this second life!',                            'translated'),
		('O.V.E.R.L.O.R.D One day...I am a villainess',                      'O.V.E.R.L.O.R.D One day...I am a villainess',                                     'translated'),
		('Quick Transmigration: Rescuing the Supporting Character',          'Quick Transmigration: Rescuing the Supporting Character',                         'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False