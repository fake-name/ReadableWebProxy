def extractIdleturtleTranslationsCom(item):
	'''
	Parser for 'idleturtle-translations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('clwp',       'Crossing to Live in the Wilderness Plains',                      'translated'),
		('Bad',        'Back to the Age of Dinosaurs',                      'translated'),
		('rse',        '[Rebirth] Sword Edge',                      'translated'),
		('rtf',        '[Rebirth] Sword Edge',                      'translated'),
		('btp',        'Back to the Peak',                      'translated'),
		('bun',        'Break Up, Next',                      'translated'),
		('teld',       'Two or Three Events in the Last Days ',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False