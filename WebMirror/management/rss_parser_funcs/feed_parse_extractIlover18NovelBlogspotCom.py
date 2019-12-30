def extractIlover18NovelBlogspotCom(item):
	'''
	Parser for 'ilover18novel.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Kedamono wa Emono ga Kakaruno wo Matte Iru ~Aoi Hitomi ni Watashi no Subete ga Abakare Chau~',             'Kedamono wa Emono ga Kakaruno wo Matte Iru ~Aoi Hitomi ni Watashi no Subete ga Abakare Chau~',             'translated'),
		('Akuma to Watashi no Yajirushi Koi Monogatari',                'Akuma to Watashi no Yajirushi Koi Monogatari',                'translated'),
		('Rikishi no Tsuma ni Sare Sou Desu (Namida)',                  'Rikishi no Tsuma ni Sare Sou Desu (Namida)',                  'translated'),
		('Enami-kun wa Watashi ni Shika Natsukanai.',                   'Enami-kun wa Watashi ni Shika Natsukanai.',                   'translated'),
		('Romance ni Hime wa Fuzai ~Shou akuma Ikusei Chuu~',           'Romance ni Hime wa Fuzai ~Shou akuma Ikusei Chuu~',           'translated'),
		('Hitotsu Yane no Shita de… Kiraina Aitsu no Amai Yuuwaku',     'Hitotsu Yane no Shita de… Kiraina Aitsu no Amai Yuuwaku',     'translated'),
		('The Prey of Zhai Wang',                                       'The Prey of Zhai Wang',                                       'translated'),
		('It’s Purely an Accident to Love Again',                       'It\'s Purely an Accident to Love Again',                      'translated'),
		('Ookami Darling Koakuma Honey',                                'Ookami Darling Koakuma Honey',                                'translated'),
		('Zenbu Oshiete Yaru yo Kacho Watashi wo Shitsukete Kudasai',   'Zenbu Oshiete Yaru yo Kacho Watashi wo Shitsukete Kudasai',   'translated'),
		('Yajuu Shikkaku ~Gogo 5 Ji Kara no Mikkai Lesson~',            'Yajuu Shikkaku ~Gogo 5 Ji Kara no Mikkai Lesson~',            'translated'),
		('Yagami-senpai no Himitsu',                                    'Yagami-senpai no Himitsu',                                    'translated'),
		('Nurete Yorokobe',                                             'Ore ni Kashizuke, Nurete Yorokobe',                           'translated'),
		('Ore ni Kashizuke',                                            'Ore ni Kashizuke, Nurete Yorokobe',                           'translated'),
		('Amai Shizuku wo Nomihoshite ~Shojo wo Musaboru Vampire~',     'Amai Shizuku wo Nomihoshite ~Shojo wo Musaboru Vampire~',     'translated'),
		('Seiryaku Kekkon Zentei?! Mitsuai no Gishiki',                 'Seiryaku Kekkon Zentei?! Mitsuai no Gishiki',                 'translated'),
		('Boku no Menomaede ● ● Koui wo Shitemite Kudasai',             'Boku no Menomaede ● ● Koui wo Shitemite Kudasai',             'translated'),
		('Ore wa Do S (Nise) ~ Chotto Hen Dayo',                        'Ore wa Do S (Nise) ~ Chotto Hen Dayo',                        'translated'),
		('Gokujou Kyoudai Harem Himitsu no Jouji',                      'Gokujou Kyoudai Harem Himitsu no Jouji',                      'translated'),
		('Yoshiwara Yuugi ~Oiran Otome no Kindan no Koi~',              'Yoshiwara Yuugi ~Oiran Otome no Kindan no Koi~',              'translated'),
		('Asahina-san no Konyaku Jijou ―4 Ninda Nante Kiitenai!―',      'Asahina-san no Konyaku Jijou ―4 Ninda Nante Kiitenai!―',      'translated'),
		('Kakusareta Aiyoku ~Kimi no Subete ga Ore no Mono~',           'Kakusareta Aiyoku ~Kimi no Subete ga Ore no Mono~',           'translated'),
		('Ichizuna Takita-kun wa Futatabi Idakanai',                    'Ichizuna Takita-kun wa Futatabi Idakanai',                    'translated'),
		('It\'s Purely an Accident to Love Again',                      'It\'s Purely an Accident to Love Again',                      'translated'),
		('The Sparrow Reluctantly Upon The Branch',                     'The Sparrow Reluctantly Upon The Branch',                     'translated'),
		('Who Allowed You to Get on the Bed',                           'Who Allowed You to Get on the Bed',                           'translated'),
		('PRC',                                                         'PRC',                                                         'translated'),
		('Loiterous', 'Loiterous',                                      'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False