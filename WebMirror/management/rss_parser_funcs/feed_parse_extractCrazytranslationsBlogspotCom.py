def extractCrazytranslationsBlogspotCom(item):
	'''
	Parser for 'crazytranslations.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('The Road To Slaying God: Chapter',   'The Road To Slaying God',      'translated'), 
		('The Road To Slaying God : Chapter',  'The Road To Slaying God',      'translated'), 
		('The Road To Slaying God :Chapter',   'The Road To Slaying God',      'translated'), 
		('The Road To Slaying God - Chapter',  'The Road To Slaying God',      'translated'), 
		('The Road To slaying God: Chaper',  'The Road To Slaying God',      'translated'), 
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False