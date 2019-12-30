def extractCarnationscansWeeblyCom(item):
	'''
	Parser for 'carnationscans.weebly.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('According to Rumors',                                                                                                     'According to Rumors, He Seems to be Trash.',                                                     'translated'),
		('Mastering Magic in an Otome Game',                                                                                        'Reincarnated into an Otome Game? Who Cares! I’m Too Busy Mastering Magic!',                      'translated'),
		('The Villainess Wants to Marry a Commoner',                                                                                'The Villainess Wants to Marry a Commoner',                                                       'translated'),
		('The Result of Being Reincarnated is Having a Master-Servant Relationship with the Yandere Love Interest Web Novel',       'The Result of Being Reincarnated is Having a Master-Servant Relationship with the Yandere Love Interest Web Novel',                      'translated'),
		('The Eternal World ~ For Whose Sake is this Story For ~',                                                                  'The Eternal World ~ For Whose Sake is this Story For ~',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False