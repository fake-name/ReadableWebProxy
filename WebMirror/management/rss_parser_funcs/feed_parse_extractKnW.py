def extractKnW(item):
	"""
	# Groups involved in KnW:
	# 	Blazing Translations
	# 	CapsUsingShift Tl
	# 	Insignia Pierce
	# 	Kiriko Translations
	# 	Konjiki no Wordmaster
	# 	Loliquent
	# 	Blazing Translations
	# 	Pummels Translations
	# 	XCrossJ
	# 	Probably another dozen randos per week.
	# Really. Fuck you people. Tag your shit, and start a group blog.

	"""
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	tags = item['tags']
	title = item['title']
	src = item['srcname']
	postfix = ''
	if src == 'XCrossJ' and 'Cross Gun' in item['tags']:
		return buildReleaseMessageWithType(item, 'Cross Gun', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Character Analysis' in item['title']:
		return False
	if 'Chapter' in title and src == 'Blazing Translations':
		if 'By:' in title:
			return False
		if 'Comment' in title:
			return False
		if ':' in title:
			postfix = title.split(':', 1)[-1].strip()
		elif '-' in title:
			postfix = title.split('–', 1)[-1].strip()
		else:
			postfix = ''
		return buildReleaseMessageWithType(item, 'Konjiki no Wordmaster', vol, chp, frag=frag, postfix=postfix)
	if ('Chapters' in tags and 'Konjiki no Wordmaster' in tags or 'Konjiki no Wordmaster Web Novel Chapters' in tags or 'Konjiki' in tags or src == 'Loliquent' and 
	    'Konjiki no Wordmaster' in title):
		postfix = title.split('–', 1)[-1].strip()
		return buildReleaseMessageWithType(item, 'Konjiki no Wordmaster', vol, chp, frag=frag, postfix=postfix)
	elif 'Konjiki no Wordmaster Chapters' in tags or 'Konjiki no Moji Tsukai' in tags or src == 'Kiriko Translations' and ('KnW' in tags or 'KnW Chapter' in title
	    ) or src == 'CapsUsingShift Tl' and 'Konjiki no Wordmaster' in title or src == 'Pummels Translations' and 'Konjiki no Word Master Chapter' in title or src == 'XCrossJ' and 'Konjiki no Moji Tsukai' in title or src == 'Insignia Pierce' and 'Konjiki no Word Master Chapter' in title:
		postfix = title.split(':', 1)[-1].strip()
		return buildReleaseMessageWithType(item, 'Konjiki no Wordmaster', vol, chp, frag=frag, postfix=postfix)
	return False
