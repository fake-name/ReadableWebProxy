def extractNovitranslation(item):
	"""
	Novels Translation
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		

	tagmap = {
		'The Evil Prince and his Precious Wife: The Sly Lady'        : 'The Evil Prince and his Precious Wife: The Sly Lady',
		'Soaring Towards the Heavens'                                : 'Soaring Towards the Heavens',
		'One Child Two Treasures: The Billionaire Chief’s Good Wife' : 'One Child Two Treasures: The Billionaire Chief’s Good Wife',
		'OCTT'                                                       : 'One Child Two Treasures: The Billionaire Chief’s Good Wife',
		'The Demon God Pesters: The Ninth Lady of the Doctor'        : 'The Demon God Pesters: The Ninth Lady of the Doctor',
		'The Mighty Female Immortal'                                 : 'The Mighty Female Immortal',
		'The pygmalion is planting seeds'                            : 'The pygmalion is planting seeds',
		'The Sacred Burial Grounds'                                  : 'The Sacred Burial Grounds',
		'The Only Starlight'                                         : 'The Only Starlight',
		'captivated by you'                                          : 'Captivated by You',
		'My Dead Husband'                                            : 'My Dead Husband',
		'Evil-Natured Husband, Don\'t Tease!'                        : 'Evil-Natured Husband, Don\'t Tease!',
		'Scapegoat Sister Vs Second Prince'                          : 'Scapegoat Sister Vs Second Prince',
		'World of Xianxia'                                           : 'World of Xianxia',
		'I heard you are an alien'                                   : 'I heard you are an Alien',
		'Good Morning Miss Ghost'                                    : 'Good Morning Miss Ghost',
		'Princess Medical Doctor'                                    : 'Princess Medical Doctor',
		'PMD'                                                        : 'Princess Medical Doctor',
		'Scapegoat Sister'                                           : 'Scapegoat Sister',
		'the demon'                                                  : 'The Demon',
		'Gifting You With A City that Will Never Be Isolated'        : 'Gifting You With A City that Will Never Be Isolated',
	}

	for tag, sname in tagmap.items():
		if tag in item['tags']:
			return buildReleaseMessageWithType(item, sname, vol, chp, frag=frag)
		
		
	return False