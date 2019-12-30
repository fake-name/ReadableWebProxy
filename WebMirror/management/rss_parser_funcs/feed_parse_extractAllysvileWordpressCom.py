def extractAllysvileWordpressCom(item):
	'''
	Parser for 'allysvile.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('jitsuwa ore, saikyōdeshita? ~ tensei chokugo wa donzoko sutāto, demo ban\'nō mahō de gyakuten jinsei o jōshō-chū!',       'Jitsuwa ore, Saikyōdeshita? ~ Tensei Chokugo wa Donzoko Sutāto, Demo Ban\'nō Mahō de Gyakuten Jinsei o Jōshō-chū!',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False