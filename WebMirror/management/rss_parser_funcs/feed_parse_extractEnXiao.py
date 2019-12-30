def extractEnXiao(item):
	"""
	Parser for 'En Xiao'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	titlemap = [
		('Who Dares Slander My Senior Brother – ',         'Who Dares Slander My Senior Brother',      'translated'),
		('Who Dares Slander My Senior Brother – Chapter',  'Who Dares Slander My Senior Brother',      'translated'),
		('Founder of Diabolism – Chapter',                 'Founder of Diabolism',                     'translated'), 
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
			
	return False