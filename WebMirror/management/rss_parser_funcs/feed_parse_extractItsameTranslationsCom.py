def extractItsameTranslationsCom(item):
	'''
	Parser for 'itsame-translations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('person with inferior ability returns from demon world',       'Person with An Inferior Ability Returning From Demon World',                      'translated'),
		('person with inferior ability',                                'Person with An Inferior Ability Returning From Demon World',                      'translated'),
		('clearing an isekai with zero believer goddess(ln)',           'clearing an isekai with zero believer goddess (ln)',                      'translated'),
		('Noble Reincarnation',                                         'Noble Reincarnation',                      'translated'),
		('iceblade magician rules over the world',                      'iceblade magician rules over the world',                      'translated'),
		('another world is full of happiness(ln)',                      'another world is full of happiness(ln)',                      'translated'),
		('sayonara ryuusei, konnichiwa jinsei(ln)',                     'sayonara ryuusei, konnichiwa jinsei(ln)',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False