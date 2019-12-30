def extractInneedtranslationWordpressCom(item):
	'''
	Parser for 'inneedtranslation.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Itai no wa Iya',       'Itai no wa Iya nanode Bōgyo-Ryoku ni Kyokufuri Shitai to Omoimasu',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	chp_prefixes = [
			('Itai no wa Iya nanode Bōgyo-Ryoku ni Kyokufuri Shitai to Omoimasu.',       'Itai no wa Iya nanode Bōgyo-Ryoku ni Kyokufuri Shitai to Omoimasu',                'translated'),
			('Slime Tensei. Taikensha ga Youjo Elf ni Dakishimeraretemasu',              'Slime Tensei. Taikensha ga Youjo Elf ni Dakishimeraretemasu',                      'translated'),
			('Itai no Wa chapter',                                                       'Itai no wa Iya nanode Bōgyo-Ryoku ni Kyokufuri Shitai to Omoimasu',                'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False