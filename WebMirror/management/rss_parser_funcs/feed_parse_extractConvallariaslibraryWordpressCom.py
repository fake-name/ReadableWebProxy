def extractConvallariaslibraryWordpressCom(item):
	'''
	Parser for 'convallariaslibrary.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Flower Selling Girl is a Replacement Bride',                      'The Flower Selling Girl is a Replacement Bride',                        'translated'),
		('Destination of Crybird',                                              'Destination of Crybird',                                                'translated'),
		('Marietta-hime no Konrei',                                             'Marietta-hime no Konrei',                                               'translated'),
		('Observation Record of A Self-Proclaimed Villainess\' Fiance',         'Observation Record of A Self-Proclaimed Villainess\' Fiancee',          'translated'),
		('Observation Record of A Self-Proclaimed Villainess\' Fiancee',        'Observation Record of A Self-Proclaimed Villainess\' Fiancee',          'translated'),
		('Different World Gender Change',                                       'Different World Gender Change',                                         'translated'),
		('Watashi wa Teki ni Narimasen!',                                       'Watashi wa Teki ni Narimasen!',                                         'translated'),
		('But God Forced Me to Reincarnate',                                    'But God Forced Me to Reincarnate',                                      'oel'),
		('Returning to the Other World with My Children',                       'Returning to the Other World with My Children',                         'oel'),
		('taking over villainess body',                                         'Taking Over the Villainess\' Body: 365 Days to Live As I Like!',        'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if 'the small sage will try her best in the different world from lv.1!' in item['tags'] and chp != 1:
		return buildReleaseMessageWithType(item, "the small sage will try her best in the different world from lv.1!", vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False