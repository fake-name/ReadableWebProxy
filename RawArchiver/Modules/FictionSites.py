
import urllib.parse
import RawArchiver.ModuleBase

class BooksieRawModule(RawArchiver.ModuleBase.RawScraperModuleBase):

	module_name = "BooksieRawModule"

	target_urls = [
		'http://www.booksie.com/',
	]

	target_tlds = [urllib.parse.urlparse(tmp).netloc for tmp in target_urls]

	badwords = [
			"/poetry",
			"/poetry/",
			"/users/",
			"/rss/",
			"/writers",
			"/pdf/",

			'/bookshelf-recommended/',
			'/member/connect?',
			'_USER_PROFILE__',
			'_MEDIA_IMAGE__120x120.',
			# Booksie tags can apparently nest arbitrarily, so
			# they basically take over the scraper if left unchecked.
			"/tags/",

	]

	@classmethod
	def cares_about_url(cls, url):
		if any([badword in url for badword in cls.badwords]):
			return False

		if RawArchiver.ModuleBase.duplicate_path_fragments(url):
			return False
		return urllib.parse.urlparse(url).netloc in cls.target_tlds

	@classmethod
	def get_start_urls(cls):
		return [tmp for tmp in cls.target_urls]

class WattPadRawModule(RawArchiver.ModuleBase.RawScraperModuleBase):

	module_name = "WattPadRawModule"

	target_urls = [
		'http://www.wattpad.com/',
	]

	target_tlds = [urllib.parse.urlparse(tmp).netloc for tmp in target_urls]

	badwords = [
			"/poetry",
			"/poetry/",
			"/users/",
			"/rss/",
			"/writers",
			"/pdf/",

			'/bookshelf-recommended/',
			'/member/connect?',
			'_USER_PROFILE__',
			'_MEDIA_IMAGE__120x120.',
			# Booksie tags can apparently nest arbitrarily, so
			# they basically take over the scraper if left unchecked.
			"/tags/",
			# People's fucked up markup leading to loops
			'tranquility_files/tranquility_files/tranquility_files',
			'nikita_files/nikita_files/nikita_files/nikita_files/nikita_files',
			'i ask myself_files/i ask myself_files/I ask myself_files',
			'what is the meaning of life_files/What is the meaning of life_files',
			'dawn of the hero 3_files/dawn of the hero 3_files/Dawn of the hero 3_files',
			'The Difference Between Right and Wrong_files/The Difference Between Right and Wrong_files',

	]

	@classmethod
	def cares_about_url(cls, url):
		if any([badword in url for badword in cls.badwords]):
			return False

		if RawArchiver.ModuleBase.duplicate_path_fragments(url):
			return False
		return urllib.parse.urlparse(url).netloc in cls.target_tlds

	@classmethod
	def get_start_urls(cls):
		return [tmp for tmp in cls.target_urls]


class FictionPressRawModule(RawArchiver.ModuleBase.RawScraperModuleBase):

	module_name = "FictionPressRawModule"

	target_urls = [
		"http://www.fictionpress.com",
		"https://www.fanfiction.net",
		"http://www.fanfiction.net",
	]

	target_tlds = [urllib.parse.urlparse(tmp).netloc for tmp in target_urls]

	badwords = [
			"/poetry",
			"/poetry/",
			"/users/",
			"/rss/",
			"/writers",
			"/pdf/",

			'/bookshelf-recommended/',
			'/member/connect?',
			'_USER_PROFILE__',
			'_MEDIA_IMAGE__120x120.',
			# FictionPress tags can apparently nest arbitrarily, so
			# they basically take over the scraper if left unchecked.
			"/tags/",

			"/post.php?",
			"/author.php?",

			"www.fashionmodeldirectory.com",
			"www.watchingprivatepractice.com",
			"Ebonyimages.jupiterimages.com",
			"www.myspace.com",
			"www.xanga.com",
			"deirdreflint.com",

			"/heroines have it hard_files/",
			"/the founders_files/",
			"/lala land_files/",
			"/the locket_files/",
			"/chasm in the forest_files/",
			"/poultrygeist the eggacy_files/",
			'/www.friendster.com/',
			'/I always loved you_files/',
			'/g-wing dating service_files/',

			"/ and ebonyimages.fashionmodeldirectory.com/",
			"/ and ebonyimages.jupiterimages.com/",
			"/ class/",
			"/ http:/",
			"/ https:/",
			"/ only in your dreams</",
			"/001 lily evans_files/",
			"/12014582/",
			"/411403/",
			"/a love, a land_files/",
			"/a new revelation_files/",
			"/a promise to be kept_files/",
			"/a slayers christmas carol_files/",
			"/a twist of fate_files/",
			"/absence of fear 1_files/",
			"/acquaintances_files/",
			"/addye_files/",
			"/adventure of a lifetime_files/",
			"/afss ch. 3_files/",
			"/afss ch. 5_files/",
			"/afss ch. 6_files/",
			"/afss ch. 8_files/",
			"/aftermath_files/",
			"/altered mirror 6_files/",
			"/an alternate life p-2_files/",
			"/an alternate reality story 1-6_files/",
			"/an attempt to save tenchi (2)_files/",
			"/an attempt to save tenchi.htlm_files/",
			"/angels on heaven and earth_files/",
			"/anotherstory2_files/",
			"/archiveofourown.org/",
			"/as much girl as you want_files/",
			"/ashen 2_files/",
			"/assassin1_files/",
			"/attack of the mary sues_files/",
			"/azkaban_files/",
			"/battles of love_files/",
			"/before the rainbow_files/",
			"/black on black1_files/",
			"/briefing room_files/",
			"/catmas1_files/",
			"/catmas2_files/",
			"/cftm1_files/",
			"/chapter 14_files/",
			"/chapter four_files/",
			"/chapter9_files/",
			"/chareif4_files/",
			"/chareif_files/",
			"/chasm in the forest_files/",
			"/chicken moon_files/",
			"/chomikuj.pl/",
			"/christmas part 1_files/",
			"/christmas2000_files/",
			"/christmas@horizon_files/",
			"/christmas@horizonp4_files/",
			"/clone2_files/",
			"/common/",
			"/convertible/",
			"/curtaincall_files/",
			"/daine's wedding_files/",
			"/dancing love5_files/",
			"/dear diary_files/",
			"/detail/",
			"/dilandau_files/",
			"/disclaime1_files/",
			"/document_files/",
			"/dog days of winter1_files/",
			"/dog days of winter2_files/",
			"/don't bug me_files/",
			"/dramatis personae_files/",
			"/dramatis persone 2_files/",
			"/dreamers awaken_files/",
			"/due to popular demand i_files/",
			"/duo's serenity p-2_files/",
			"/e_t_ go home!!!_files/",
			"/end_files/",
			"/eponine_files/",
			"/exterior/",
			"/eyes on me_files/",
			"/fanfic1_files/",
			"/fanfiction.com.br/",
			"/fic35_files/",
			"/finalfantasy high_files/",
			"/findingapath10_files/",
			"/findingapath1_files/",
			"/firstkiss_files/",
			"/flowergirl_files/",
			"/for better or for worse_files/",
			"/freaky friday_files/",
			"/friendship_files/",
			"/from light into darkness_files/",
			"/fruit wars_files/",
			"/fy_sweetlove_1_files/",
			"/g-wing dating service_files/",
			"/gcag1a_files/",
			"/gcag3a_files/",
			"/gray_files/",
			"/guardians part 1_files/",
			"/gumdam wing_files/",
			"/gundam humorii_files/",
			"/has1_files/",
			"/heroines have it hard_files/",
			"/historia/",
			"/home is where the heart is_files/",
			"/how green was my lisa_files/",
			"/hp5-pt 1_files",
			"/hp5-pt 1_files/",
			"/hpandthepottetes_files/",
			"/i always loved you_files/",
			"/i can't let go ch 3_files/",
			"/i don_files/",
			"/i had no choice_files/",
			"/i will survive_files/",
			"/i'm poed at vegeta!_files/",
			"/i_files/",
			"/if i went to hogwarts_files/",
			"/immortality1_files/",
			"/in your darkest hour ch21 finale_files/",
			"/instagram.com/",
			"/into the light_files/",
			"/it's my life- neville_files/",
			"/jcsfh_files/",
			"/jerry_files/",
			"/jfgbarry_files/",
			"/jinxed 1_files/",
			"/kingcrabshippingjackxyusei.wikia.com/",
			"/krelboyne hell part 1_files/",
			"/krelboyne hell part 2_files/",
			"/lala land_files/",
			"/lasthope ch.4_files/",
			"/light to darkness-rainbow4_files/",
			"/ll and v_files/",
			"/lois on the warpath part 1_files/",
			"/lois on the warpath part 2_files/",
			"/love never dies_files/",
			"/lucas death_files/",
			"/majare_files/",
			"/matt+sora=luv part 3_files/",
			"/maxi11_files/",
			"/maxi8_files/",
			"/maxi9_files/",
			"/mcgundam's_files/",
			"/mimi_files/",
			"/mitmfanfic1_files/",
			"/mitmfanfic3_files/",
			"/model/",
			"/never mind me.files/",
			"/nobody wants to be lonely_files/",
			"/not alone anymore_files/",
			"/notwithoutyou_files/",
			"/once and again 9_files/",
			"/outsideff_files/",
			"/part 1_files/",
			"/part a (revised)_files/",
			"/piccolo's pics/",
			"/please let go ch 1_files/",
			"/pleaseworksoicanbreathe_files/",
			"/plus dolye - parting gifts_files/",
			"/poem1_files/",
			"/pokeshow2_files/",
			"/pokeshow3_files/",
			"/poor old 4 privet drive_files/",
			"/poultrygeist the eggacy_files/",
			"/power over me prt.1_files/",
			"/power over me prt.2_files/",
			"/pretty as a picture_files/",
			"/princessdream4_files/",
			"/quina_files/",
			"/ragwp_files/",
			"/rainy day pt3_files/",
			"/rebirth_files/",
			"/ringing in the new year part 1_files/",
			"/rini&pluto_files/",
			"/ron's moment with lockhart_files/",
			"/rosepro_files/",
			"/saiyans_files/",
			"/sandandwater4_files/",
			"/scott and shelby unlmtd. ch1_files/",
			"/secure part one_files/",
			"/serenabday1_files/",
			"/she was a good wife_files/",
			"/site/",
			"/sites.google.com/",
			"/slytherinsong_files/",
			"/snow buildin'_files/",
			"/solstice_files/",
			"/something worth fighting for internet_files/",
			"/sometimes thing just turn out that way- part 3_files/",
			"/sorcerer hunters darling make love to me_files/",
			"/sorcerer hunters don't leave me darling_files/",
			"/special class part 1_files/",
			"/spring_files/",
			"/stars on ice prologue_files/",
			"/stonesickness3_files/",
			"/story2_files/",
			"/tama_files/",
			"/tenchi muyo no need to blow up the masaki house_files/",
			"/the baudelaire orphans looked up at their new home_files/",
			"/the emporor and the frog_files/",
			"/the endgame chapters_files/",
			"/the endless dance continues 1_files/",
			"/the endless dance continues 2_files/",
			"/the founders_files/",
			"/the ghost of christmas past_files/",
			"/the locket_files/",
			"/the long road home_files/",
			"/the mysterious girl_files/",
			"/the race_files/",
			"/the reawakening-dbzp_files/",
			"/the way home scott2_files/",
			"/the way home shelby_files/",
			"/the zone_files/",
			"/the_beginnings_files/",
			"/thechillofdeath_files/",
			"/theprincess_files/",
			"/thevenusspell_files/",
			"/this is going to be my weirdest fic ever_files/",
			"/thistlepaws/",
			"/together_files/",
			"/transformed00_files/",
			"/trapped_files/",
			"/trying to forget_files/",
			"/um_dia_na_terraum_novo_amor/",
			"/unspoken truth by_files/",
			"/untitledasofyet2_files/",
			"/users/",
			"/vacation1_files/",
			"/valentines part 1_files/",
			"/valentinesjewelle_files/",
			"/viole_files/",
			"/voice of distortion_files/",
			"/voldemort barbie girl_files/",
			"/walk_files/",
			"/waterloo_files/",
			"/weheartit.com/",
			"/westwingcj1_files/",
			"/what can i do to make you love me6_files/",
			"/what does it take_files/",
			"/why final fantasy never made it as tv stars_files/",
			"/why goodbye-story-dateien/",
			"/why_files/",
			"/wiki/",
			"/wilson1_files/",
			"/winter_files/",
			"/www.fanfiction.net/",
			"/www.fictionpress.com/",
			"/www.friendster.com/",
			"/yushepi_files/",

	]

	@classmethod
	def cares_about_url(cls, url):
		if any([badword in url for badword in cls.badwords]):
			return False

		if RawArchiver.ModuleBase.duplicate_path_fragments(url):
			return False
		return urllib.parse.urlparse(url).netloc in cls.target_tlds

	@classmethod
	def get_start_urls(cls):
		return [tmp for tmp in cls.target_urls]

