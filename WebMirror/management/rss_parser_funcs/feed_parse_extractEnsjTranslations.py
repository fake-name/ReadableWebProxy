def extractEnsjTranslations(item):
	"""
	# Ensj Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	
	tagmap = [
		('RMB',       'Record of Muwui’s Battles',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	if 'Tutorials' in item['tags']:
		return None
		
	if 'King Shura' in item['tags']:
		return buildReleaseMessageWithType(item, 'King Shura', vol, chp, frag=frag, postfix=postfix)
	if 'I\'m Sorry For Being Born In This World!' in item['tags']:
		return buildReleaseMessageWithType(item, 'I\'m Sorry For Being Born In This World!', vol, chp, frag=frag, postfix=postfix)
	if 'The Record of a Thousand Lives' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Record of a Thousand Lives', vol, chp, frag=frag, postfix=postfix)
	if 'Running Away From The Hero!' in item['tags']:
		if not frag:
			match = re.search('\\((\\d+)\\)', item['title'])
			if match:
				frag = int(match.group(1))
		return buildReleaseMessageWithType(item, 'Running Away From The Hero!', vol, chp, frag=frag, postfix=postfix)
		
		
	titlemap = [
		('[King Shura]',      'King Shura',            'translated'),
		('Invisible dragon',  'Invisible dragon',      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False