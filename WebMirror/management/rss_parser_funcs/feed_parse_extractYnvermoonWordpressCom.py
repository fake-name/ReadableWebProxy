def extractYnvermoonWordpressCom(item):
	'''
	Parser for 'ynvermoon.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('My Childhood Friend the Demon Knight, Hates Me',          'My Childhood Friend the Demon Knight Hates Me',          'translated'),
		('Do You Think You Can Run After Reincarnating, Nii-san',  'Do You Think You Can Run After Reincarnating, Nii-san?', 'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False