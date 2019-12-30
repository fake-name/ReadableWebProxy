def extractDxhaseoxdtBlogspotCom(item):
	'''
	Parser for 'dxhaseoxdt.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False


	urlfrag = [
		('/empress-running-away-with-ball-chapter',  'Empress Running Away with the Ball!',                      'translated'),
		('/virtual-world-conquering-world-chapter',  'Virtual World: Conquering the World',                      'translated'),
		('/legend-of-asura-chapter',                 'Legend of the Asura',                                      'translated'),
		('/cold-kings-dominating-love-genius',       'Cold King\'s Dominating Love, Genius Medical Consort',     'translated'),

	]

	for key, name, tl_type in urlfrag:
		if key in item['linkUrl'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('Cold King\'s Dominating Love, Genius Medical Consort Chapter',           'Cold King\'s Dominating Love, Genius Medical Consort',          'translated'),
		('Empress Running Away with the Ball! Chapter',                            'Empress Running Away with the Ball!',                           'translated'),
		('Evil Emperor\'s Poisonous Consort: Divine Doctor Young Miss Chapter ',   'Evil Emperor\'s Poisonous Consort: Divine Doctor Young Miss',   'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False