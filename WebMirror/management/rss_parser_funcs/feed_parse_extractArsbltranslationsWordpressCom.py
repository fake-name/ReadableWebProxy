def extractArsbltranslationsWordpressCom(item):
	'''
	Parser for 'arsbltranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Picked up a Strange Knight',                    'Picked up a Strange Knight',                                   'translated'),
		('Aloof King and Cold (Acting) Queen',            'Aloof King and Cold (Acting) Queen',                           'translated'),
		('Moonlight on the Snowfield',                    'Moonlight on the Snowfield',                                   'translated'),
		('Brought My Wife Back from Another World',       'Brought My Wife Back from Another World',                      'translated'),
		('Your Kingdom',                                  'Your Kingdom',                                                 'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False