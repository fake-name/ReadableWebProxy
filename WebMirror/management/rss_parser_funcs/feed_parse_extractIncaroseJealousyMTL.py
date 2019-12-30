def extractIncaroseJealousyMTL(item):
	"""
	'Incarose Jealousy MTL'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	chp_prefixes = [
			('konyaku haki? yoroshī. naraba, fukushūda! chapter ',  'Konyaku haki? Yoroshī. Naraba, fukushūda!',   'translated'),
			('akuyaku reijō ttenani o sureba yoi nda kke? chapter', 'Akuyaku Reijō ttenani o Sureba Yoi nda kke?', 'translated'),
			('mochiron, isharyōseikyū itashimasu! chapter ',        'Mochiron, Isharyōseikyū Itashimasu!',         'translated'),
			('dare ga tame chapter ',                               'Dare ga Tame',                                'translated'),
			('The Analects of Righteous Father’s Collapse',         'The Analects of Righteous Father’s Collapse', 'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


		
	return False