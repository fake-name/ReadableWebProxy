def extractHanashiObasan(item):
	"""
	'Hanashi Oba-san'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('The Hero Suddenly Proposed to Me But',       'The Hero Suddenly Proposed to me, but…',           'translated'),
		('Hero Suddenly Proposed',                     'The Hero Suddenly Proposed to me, but…',           'translated'),
		('souryo-sama no koiwazurai',                  'A Monk\'s Lovesickness',                           'translated'),
		('Monk\'s Lovesickness',                       'A Monk\'s Lovesickness',                           'translated'),
		('Magic Academy\'s Romantic Circumstances',    'The Magic Academy\'s Romantic Circumstances',      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('Renai Jijou',    'The Magic Academy\'s Romantic Circumstances', 'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False