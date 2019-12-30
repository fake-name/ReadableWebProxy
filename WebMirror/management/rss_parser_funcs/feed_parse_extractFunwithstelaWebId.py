def extractFunwithstelaWebId(item):
	'''
	Parser for 'funwithstela.web.id'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None


	tagmap = [
		('Because The Pig Duke Has Been Reincarnated, This Time I Will Say I Like You',       'Because The Pig Duke Has Been Reincarnated, This Time I Will Say I Like You',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('Piggy Duke',  'Because The Pig Duke Has Been Reincarnated, This Time I Will Say I Like You',                      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
			
			
			
			
	return False