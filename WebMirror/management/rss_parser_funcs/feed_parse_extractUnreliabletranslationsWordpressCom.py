def extractUnreliabletranslationsWordpressCom(item):
	'''
	Parser for 'unreliabletranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	# Numeric tags are sadness
	if item['tags'] == ['5:50'] and chp != 5:
		return buildReleaseMessageWithType(item, "One Night Lovely Wife $5.50: Overwhelming Black Belly Husband", vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		
		

	tagmap = [
		('wlod',       'White Lotus Overturned Daily',                      'translated'),
		('mchtm!',       'My Chief Husband, Too Mensao!',                      'translated'),
		('vod',       'I Became the Villain\'s Own Daughter',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False