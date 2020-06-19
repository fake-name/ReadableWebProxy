def extract18FoxaholicCom(item):
	'''
	Parser for '18.foxaholic.com'
	'''

	badwords = [
			'Protected:',
			'[Patreon Only]',
		]
	if any([bad in item['title'] for bad in badwords]):
		return None


	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('av filming guidebook',                    'av filming guidebook',                                   'translated'),
		('not allowed to leak a single drop',       'not allowed to leak a single drop',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False