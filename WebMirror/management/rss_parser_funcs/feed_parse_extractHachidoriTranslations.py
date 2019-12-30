def extractHachidoriTranslations(item):
	"""
	Parser for 'Hachidori Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Charging Magic with a Smile' in item['tags']:
		return buildReleaseMessageWithType(item, 'Charging Magic with a Smile', vol, chp, frag=frag, postfix=postfix)
	if 'Kokugensou wo Item Cheat' in item['tags']:
		return buildReleaseMessageWithType(item, 'Kokugensou wo Item Cheat', vol, chp, frag=frag, postfix=postfix)
	if 'Ochitekita Naga to Majo no Kuni' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ochitekita Naga to Majo no Kuni', vol, chp, frag=frag, postfix=postfix)
	if 'Humans are the Strongest Race' in item['tags']:
		return buildReleaseMessageWithType(item, 'Humans are the Strongest Race', vol, chp, frag=frag, postfix=postfix)
	if 'Seiun wo Kakeru' in item['tags']:
		return buildReleaseMessageWithType(item, 'Seiun wo Kakeru', vol, chp, frag=frag, postfix=postfix)
	return False