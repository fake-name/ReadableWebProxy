def extractDaikyunTranslations(item):
	"""
	Daikyun Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].lower().startswith('The Annals of the Flame Kingdom'.lower()):
		return buildReleaseMessageWithType(item, 'The Annals of the Flame Kingdom', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('the evil organization’s recruitment ad '):
		return buildReleaseMessageWithType(item, 'The Evil Organization’s Recruitment Ad', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('teora –'):
		return buildReleaseMessageWithType(item, 'The Evil Organization’s Recruitment Ad', vol, chp, frag=frag, postfix=postfix)
		
	tagmap = [
		('TEORA',       'The Evil Organization’s Recruitment Ad',                      'translated'),
		('PRC',         'PRC',                      'translated'),
		('IBFDD',       'This Time, I Became the Fiance of a Duke’s Daughter. But She is Rumored to have Bad Personality, and Ten Years Older',                      'translated'),
		('Loiterous',   'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)