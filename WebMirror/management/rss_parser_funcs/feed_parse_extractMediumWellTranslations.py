def extractMediumWellTranslations(item):
	"""
	Parser for 'Medium Well Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Isekai C-Mart Hanjouki',                  'Isekai C-Mart Hanjouki',                'translated'),
		('from mightiest hero to demon king',       'From Mightiest Hero to Demon King',     'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False