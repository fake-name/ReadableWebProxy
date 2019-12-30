def extractUntunedTranslation(item):
	"""

	"""
	title = item['title'].replace(' III(', ' vol 3 (').replace(' III:', ' vol 3:').replace(' II:', ' vol 2:').replace(' I:', ' vol 1:').replace(' IV:', ' vol 4:').replace(
	    ' V:', ' vol 5:')
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(title)
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		

	tagmap = [
		('meg and seron',       'Meg and Seron', 'translated'),
		('kino\'s journey',       'Kino\'s Journey', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


		
	if 'meg and seron' in item['tags'] and chp and vol:
		return buildReleaseMessageWithType(item, 'Meg and Seron', vol, chp, frag=frag, postfix=postfix)
	if 'lillia and treize' in item['tags'] and chp and vol:
		return buildReleaseMessageWithType(item, 'Lillia to Treize', vol, chp, frag=frag, postfix=postfix)
	return False