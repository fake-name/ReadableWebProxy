def extractXianxianovelWordpressCom(item):
	'''
	Parser for 'xianxianovel.wordpress.com'
	'''
	if 'Translators Noise'.lower() in item['title'].lower():
		return None
		
		
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	chp_prefixes = [
			('Nine Yang Sword Saint',                               True,  'translated'),
			('Genius Sword Immortal',                               True,  'translated'),
			('Beast Piercing The Heavens',                          True,  'translated'),
			('Zhanxian',                                            True,  'translated'),
		]

	for series, require_chp, tl_type in chp_prefixes:
		if item['title'].lower().startswith(series.lower()) and (not require_chp or 'chapter' in item['title'].lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False