def extractAvert(item):
	"""
	# Avert Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (vol or chp or frag):
		return False
	if 'rokujouma' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Rokujouma no Shinryakusha!', vol, chp, frag=frag, postfix=postfix)
	elif 'fuyo shoukan mahou' in item['title'].lower() or 'fuyo shoukan mahou' in item['tags'] or 'fuyou shoukan mahou' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Boku wa Isekai de Fuyo Mahou to Shoukan Mahou wo Tenbin ni Kakeru', vol, chp, frag=frag, postfix=postfix)
	elif 'regarding reincarnated to slime chapter' in item['title'].lower() or 'Tensei Shitara Slime Datta Ken' in item['tags']:
		return buildReleaseMessageWithType(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)
		
	if re.match('^Release:? fuyo shoukan mahou? vol ?\\d+ chapter \\d+', item['title'], re.IGNORECASE):
		return buildReleaseMessageWithType(item, 'Boku wa Isekai de Fuyo Mahou to Shoukan Mahou wo Tenbin ni Kakeru', vol, chp, frag=frag, postfix=postfix)

		
	return False