def extractGuanatranslationsWordpressCom(item):
	'''
	Parser for 'guanatranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('PEN DOWN A MARRIAGE: CHAPTER',              'Pen Down A Marriage',      'translated'),
		('PEN DOWN A MARRIAGE (落笔成婚 ) CHAPTER',   'Pen Down A Marriage',      'translated'),
		('PEN DOWN A MARRIAGE (落笔成婚 ): CHAPTER',  'Pen Down A Marriage',      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False