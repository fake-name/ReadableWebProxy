def extractRazstlcornerWordpressCom(item):
	'''
	Parser for 'razstlcorner.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Bu ni mi',       'Bu ni Mi wo Sasagete Hyaku to Yonen. Elf de Yarinaosu Musha Shugyou (LN)',                      'translated'),
		('Bu ni Mi',       'Bu ni Mi wo Sasagete Hyaku to Yonen. Elf de Yarinaosu Musha Shugyou (LN)',                      'translated'),
		('VRMMO',          'VRMMO no Shien Shokunin ~Top player no Shikakenin~',                                            'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False