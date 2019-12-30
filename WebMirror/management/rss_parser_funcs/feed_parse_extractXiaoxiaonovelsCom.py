def extractXiaoxiaonovelsCom(item):
	'''
	Parser for 'xiaoxiaonovels.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None


	tagmap = [
		('The Girl Who Ate a Death God Side Story',        'The Girl Who Ate a Death God',                   'translated'), 
		('Yuusha, Aruiwa Bakemono to Yobareta Shoujo',     'Yuusha, Aruiwa Bakemono to Yobareta Shoujo',     'translated'), 
		('King of Myriad Domain',                          'King of Myriad Domain',                          'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			if 'The Girl Who Ate a Death God Side Story' in item['tags']:
				postfix = "Side Story"
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('RIW Chapter',                                                       "Reincarnated Into A Werewolf As The Demon King's Servant",      'translated'),
		('Reincarnated Into A Werewolf As The Demon King’s Servant Chapter',  "Reincarnated Into A Werewolf As The Demon King's Servant",      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)




	return False