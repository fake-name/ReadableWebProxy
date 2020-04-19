def extractSodapressinCom(item):
	'''
	Parser for 'sodapressin.com'
	'''
	if item['tags'] == []:
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('On the Way Home I Got a Bride and Twin Daughters, Who Were Dragons',       'On the Way Home I Got a Bride and Twin Daughters, Who Were Dragons',                      'translated'),
		('I’m Not Going to Be Bullied By a Girl',                                    'I’m Not Going to Be Bullied By a Girl',                                                   'translated'),
		('Picked up a Demon King to be a Maid',                                      'Picked up a Demon King to be a Maid',                                                     'translated'),
		('what should i do if i was forced to marry the elf queen',                  'what should i do if i was forced to marry the elf queen',                                 'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False