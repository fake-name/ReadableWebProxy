def extractTigertranslationsOrg(item):
	'''
	Parser for 'tigertranslations.org'
	'''
	
	ttmp = item['title'].replace("10 Years", "<snip> years").replace("10 Years Later", "<snip> years")

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(ttmp)
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('I Will Not Become an Enemy!',                                              'I Will Not Become an Enemy!',                                                             'translated'),
		('My Sister the Heroine, and I the Villainess',                              'My Sister the Heroine, and I the Villainess',                                             'translated'),
		('Isekai ni Kita Boku wa Kiyoubinbode Subaya-sa Tayorina Tabi o Suru',       'Isekai ni Kita Boku wa Kiyoubinbode Subaya-sa Tayorina Tabi o Suru',                      'translated'),
		('Jack of all Trades',                                                       'Isekai ni Kita Boku wa Kiyoubinbode Subaya-sa Tayorina Tabi o Suru',                      'translated'),
		('Prison Dungeon and the Exiled Hero',                                       'Prison Dungeon and the Exiled Hero',                                                      'translated'),
		('Two Saints wander off into a Different World',                             'Two Saints wander off into a Different World',                                            'translated'),
		('Lioncourt War',                                                            'A History of the Lioncourt War',                                                          'translated'),
		('realist demon king',                                                       'The Legendary Rebuilding of a World by a Realist Demon King',                             'translated'),
		('Koko wa Ore ni Makasete Saki ni Ike to Itte kara 10 Nen ga Tattara Densetsu ni Natteita',       'Koko wa Ore ni Makasete Saki ni Ike to Itte kara 10 Nen ga Tattara Densetsu ni Natteita',                      'translated'),
		('Tensei Kenja no Isekai Raifu ~Daini no Shokugyo wo Ete, Sekai Saikyou ni Narimashita',          'Tensei Kenja no Isekai Raifu ~Daini no Shokugyo wo Ete, Sekai Saikyou ni Narimashita~',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]
	
	# Handle annoying series with numbers in the title.
	if 'Koko wa Ore ni Makasete Saki ni Ike to Itte kara 10 Nen ga Tattara Densetsu ni Natteita' in item['tags'] and chp == 10:
		return False

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False