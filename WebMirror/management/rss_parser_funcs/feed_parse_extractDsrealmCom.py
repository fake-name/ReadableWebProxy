def extractDsrealmCom(item):
	'''
	Parser for 'dsrealm.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	tagmap = [
		('Reincarnated As A Dragons Egg',       'Reincarnated As A Dragons Egg',                      'translated'),
		('Dullahan',                            'I\'m a Dullahan, Looking for my Head',               'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	
	if item['title'].startswith("Chapter") and item['tags'] == ['Uncategorized']:
		return buildReleaseMessageWithType(item, "Reincarnated as a Dragon’s Egg ～Lets Aim to Be the Strongest～", vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith("News and Chapter") and item['tags'] == ['Uncategorized']:
		return buildReleaseMessageWithType(item, "Reincarnated as a Dragon’s Egg ～Lets Aim to Be the Strongest～", vol, chp, frag=frag, postfix=postfix)

	return False