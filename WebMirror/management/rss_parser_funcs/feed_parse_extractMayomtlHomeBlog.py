def extractMayomtlHomeBlog(item):
	'''
	Parser for 'mayomtl.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('My Lover Was Stolen, And I Was Kicked Out Of The Hero’s Party, But I Awakened To The EX Skill “Fixed Damage” And Became Invincible. Now, Let’s Begin Some Revenge',       
			'My Lover Was Stolen, And I Was Kicked Out Of The Hero’s Party, But I Awakened To The EX Skill “Fixed Damage” And Became Invincible. Now, Let’s Begin Some Revenge',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False