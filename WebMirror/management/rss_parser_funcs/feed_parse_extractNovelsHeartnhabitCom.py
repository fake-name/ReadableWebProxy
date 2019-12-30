def extractNovelsHeartnhabitCom(item):
	'''
	Parser for 'novels.heartnhabit.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tag_title_map = [
		('Black Belly Boss\'s Pet Wife (黑老大们的宠妻)',     'Black Belly Boss\'s Pet Wife',                                 'translated'),
		('Black Belly Boss\'s Pet Wife',                      'Black Belly Boss\'s Pet Wife',                                 'translated'),
		('LITTLE GOBLIN: Master don\'t come here!',           'LITTLE GOBLIN: Master don\'t come here!',                      'translated'),
		('LITTLE GOBLIN: Master, don’t come here!',           'LITTLE GOBLIN: Master don\'t come here!',                      'translated'),
	]

	for tagname, name, tl_type in tag_title_map:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	for titlecomponent, name, tl_type in tag_title_map:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
			
	return False