def extractYoraikun(item):
	"""
	# Yoraikun
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	snames = [
			'The Rise of the Shield Hero',
			'Konjiki no Wordmaster',
			'Sevens',
			'Dragoon',
			'The Lazy King',
			'Me, Her, and the Ballistic Weaponry [Antique]',
		]

	tlut = {tmp.lower(): tmp for tmp in snames}

	tlut['ikctawbwtwh']                      = "I Kinda Came to Another World, But Where's the Way Home"
	tlut['okitegami kyouko']                 = "The Memorandum of Okitegami Kyouko"
	tlut['battlefield masurawo']             = "Sentou Jousai Masurawo"
	tlut['the christmas of the shield hero'] = "The Rise of the Shield Hero"
	tlut['alchemuls']                        = "Waga Hero no Tame no Alchemuls"
	tlut['aura']                             = "AURA: Koga Maryuin\'s Last Battle"
	
	ltags = [tmp.lower() for tmp in item['tags']]
	for key, value in tlut.items():
		if key in ltags:
			tl_type = 'translated'

			return buildReleaseMessageWithType(item, value, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	
	titlemap = [
		('Mary-san Comes on Foot',  'Mary Comes on Foot',      'translated'), 
		('Mary Comes on Foot',      'Mary Comes on Foot',      'translated'), 
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False