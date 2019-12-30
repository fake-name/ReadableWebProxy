def extractKONDEETranslations(item):
	"""
	#'KONDEE Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
		
	tagmap = [
		('Sakyubasu ni Tensei Shitanode Miruku o Shiborimasu',       'Sakyubasu ni Tensei Shitanode Miruku o Shiborimasu',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	titlemap = [
		('Rune Troopers',                                                'Rune Troopers',                                                   'translated'),
		('SUCCUBUS NI TENSEI SHITANODE MIRUKU WO SHIBORIMASU ',          'Sakyubasu ni tensei shitanode miruku o shiborimasu',              'translated'),
		('SAKYUBASU NI TENSEI SHITANODE MIRUKU O SHIBORIMASU ',          'Sakyubasu ni tensei shitanode miruku o shiborimasu',              'translated'),
		('Omae wo Otaku ni Shiteyaru kara, Ore wo Riajuu ni Shitekure!', 'Omae o Otaku ni Shiteyaru kara, Ore o Riajuu ni Shitekure!',      'translated'),
		('Omae o otaku ni shiteyaru kara, ore o riajuu ni shitekure!',   'Omae o Otaku ni Shiteyaru kara, Ore o Riajuu ni Shitekure!',      'translated'),
		('Omae wo Otaku ni Shiteyarukara Ore wo Riajuu ni Shitekure',    'Omae o Otaku ni Shiteyaru kara, Ore o Riajuu ni Shitekure!',      'translated'),
		('Omae o otaku ni shiteyaru kara ore o riajuu ni shitekure',     'Omae o Otaku ni Shiteyaru kara, Ore o Riajuu ni Shitekure!',      'translated'),
		('Chuuko Demo Koi ga Shitai',                                    'Chuuko demo Koi ga Shitai!',                                      'translated'), 
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False