def extractDominantprogrammerWordpressCom(item):
	'''
	Parser for 'dominantprogrammer.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Reincarnation Hypnosis Ability',                                                                'I, Who had Arrived in Another World, Will Live As I Like With My Hypnosis Ability',     'translated'),
		('I, Who had Arrived in Another World, Will Live As I Like With My Hypnosis Ability',             'I, Who had Arrived in Another World, Will Live As I Like With My Hypnosis Ability',     'translated'),
		('Mind Controlling My Childhood Friend, I Made Her My Sex Slave',                                 'Mind Controlling My Childhood Friend, I Made Her My Sex Slave',                         'translated'),
		('Eroge Reincarnation ~Please Don\'t Collect Onee-chan\'s CGs~',                                  'Eroge Reincarnation ~Please Don\'t Collect Onee-chan\'s CGs~',                          'translated'),
		('Saimin Regulation',                                                                             'Saimin Regulation',                                                                     'translated'),
		('As The Spirit-Sama Says',                                                                       'As The Spirit-Sama Says',                                                               'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False