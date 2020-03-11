def extractRequiemtranslationsWordpressCom(item):
	'''
	Parser for 'requiemtranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('villainess\' father',                  'Since I’ve Reincarnated as the Villainess\' Father, I’ll Shower My Wife and Daughter in Love',                              'translated'), 
		('Shiro Buta Reijou',                  'Tensei Saki ga Shoujo Manga no Shiro Buta Reijou datta',                                                                      'translated'), 
		('Fiance of a Duke\'s Daughter',       'This Time, I Became the Fiance of a Duke’s Daughter. But She is Rumored to have a Bad Personality, and is Ten Years Older',   'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False