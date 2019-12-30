def extractWuxiaSociety(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if '/forum/viewtopic.php' in item['linkUrl']:
		return None
	if 'The Heaven Sword and Dragon Sabre' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'The Heaven Sword and Dragon Sabre', vol, chp, frag=frag, postfix=postfix)
		
	tagmap = [
		('A Martial Odyssey',                       'A Martial Odyssey',                                      'translated'),
		('The Heaven Sword and Dragon Sabre',       'The Heaven Sword and Dragon Sabre',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False