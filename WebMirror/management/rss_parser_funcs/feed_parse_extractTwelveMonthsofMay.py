def extractTwelveMonthsofMay(item):
	"""
	# 'Twelve Months of May'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'My Mister Ostrich' in item['tags']:
		return buildReleaseMessageWithType(item, 'Wo De Tuo Niao Xian Sheng', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Ostrich Chapter'):
		return buildReleaseMessageWithType(item, 'Wo De Tuo Niao Xian Sheng', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('My Fault For Being Blind') or 'My Fault For Being Blind' in item['tags']:
		return buildReleaseMessageWithType(item, 'Zhi Guai Dang Chu Xia Le Yan', vol, chp, frag=frag, postfix=postfix)
	if 'Split Zone No.13' in item['tags']:
		return buildReleaseMessageWithType(item, 'Split Zone No.13', vol, chp, frag=frag, postfix=postfix)
	if 'The Lighter and Princess Gown' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Lighter and Princess Gown', vol, chp, frag=frag, postfix=postfix)
	if 'Lighter & Princess Gown' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Lighter and Princess Gown', vol, chp, frag=frag, postfix=postfix)
	return False