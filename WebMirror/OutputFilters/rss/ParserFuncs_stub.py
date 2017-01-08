
# pylint: disable=C0112,R0911,R0912,W0612


from WebMirror.OutputFilters.util.MessageConstructors import buildReleaseMessage
from WebMirror.OutputFilters.util.TitleParsers import extractChapterVol
from WebMirror.OutputFilters.util.TitleParsers import extractChapterVolFragment
from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix

import re

####################################################################################################################################################
#
####################################################################################################################################################
def extractWIP(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	print(item['title'])
	print(item['tags'])
	print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractNop(dummy_item):
	'''

	'''

	return None



####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################


def extractACupofMemory(item):
	'''
	'A Cup of Memory'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractALittleMirageTranslation(item):
	'''
	'A Little Mirage Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractABCpwip(item):
	'''
	'ABCpwip'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractAfterTranslations(item):
	'''
	'After;Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractAiHristDreamTranslations(item):
	'''
	'Ai Hrist Dream Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractAlpenGlowTranslations(item):
	'''
	'Alpen Glow Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractAndromedaBoul(item):
	'''
	'Andromeda & Boul'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractAnkydonsLair(item):
	'''
	"Ankydon's Lair"
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractBLNovelObsession(item):
	'''
	'BL Novel Obsession'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractChauffeurTranslations(item):
	'''
	'Chauffeur Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractChoyceClub(item):
	'''
	'Choyce.club'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractChroniclesofGaia(item):
	'''
	'Chronicles of Gaia'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractDailyDoseNovels(item):
	'''
	'Daily Dose Novels'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractDrakeTranslations(item):
	'''
	'Drake Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractDuskTales(item):
	'''
	'Dusk Tales'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractEndofthedays42(item):
	'''
	'End of the days42'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractEveningBoatTranslations(item):
	'''
	'Evening Boat Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractFeelsBadTranslation(item):
	'''
	'Feels Bad Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractFriendshipIsPower(item):
	'''
	'Friendship Is Power'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractHalcyonTranslations(item):
	'''
	'Halcyon Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractHanashiObasan(item):
	'''
	'Hanashi Oba-san'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractHecatesCorner(item):
	'''
	"Hecate's Corner"
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractHirikasMTs(item):
	'''
	"Hirika's MTs"
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractIAmABananaFreshieTranslation(item):
	'''
	'IAmABanana Freshie Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractIansCorner(item):
	'''
	"Ian's Corner"
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractInaccurateTranslations(item):
	'''
	'Inaccurate Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractIncaroseJealousyMTL(item):
	'''
	'Incarose Jealousy MTL'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractInfinityTranslations(item):
	'''
	'Infinity Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractIsekaiFiction(item):
	'''
	'Isekai Fiction'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractJawzPublications(item):
	'''
	'Jawz Publications'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractJunkBurstTranslations(item):
	'''
	'Junk Burst Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractKakaooStory(item):
	'''
	'Kakaoo Story'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractKazamaTranslation(item):
	'''
	'Kazama Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractKenkyoReika(item):
	'''
	'Kenkyo Reika'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractKhasinTH(item):
	'''
	"kha'sinTH"
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractKidneyTranslations(item):
	'''
	'Kidney Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractKitaKamiOoi(item):
	'''
	'KitaKami Ooi'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractKuroTranslation(item):
	'''
	'Kuro Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractLaughingGhoulTranslations(item):
	'''
	'Laughing Ghoul Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractLazyGTranslations(item):
	'''
	'Lazy G Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractLightNovelswithMisachan(item):
	'''
	'Light Novels with Misa-chan~'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractLogatseTranslations(item):
	'''
	'Logatse Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractLovelyxDay(item):
	'''
	'Lovely x Day'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractLuminaeris(item):
	'''
	'Luminaeris'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractMyBrainsArt(item):
	'''
	"My Brain's Art"
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractMyFirstTimeTranslating(item):
	'''
	'My First Time Translating'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractNextlevelforthePLOT(item):
	'''
	'Next level for the PLOT'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractNieracolTranslations(item):
	'''
	'Nieracol Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractNinthCharmolypiTranslation(item):
	'''
	'Ninth Charmolypi Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractNorvaBlog(item):
	'''
	'Norva Blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractNovellaTranslation(item):
	'''
	'Novella Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractOOOTranslations(item):
	'''
	'OOO Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractOppaTranslations(item):
	'''
	'OppaTranslations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractOrangeTranslations(item):
	'''
	'Orange Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractOrinjidoScans(item):
	'''
	'Orinjido Scans'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractOtsumi(item):
	'''
	'Otsumi'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractParadoxTranslations(item):
	'''
	'Paradox Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractParaphraseTranslation(item):
	'''
	'Paraphrase Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractPegasusFarts(item):
	'''
	'Pegasus Farts'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractPFCLightNovelTranslations(item):
	'''
	'PFC – Light Novel Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractPlantTranslation(item):
	'''
	'Plant Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractProductiveProcrastination(item):
	'''
	'Productive Procrastination'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractProfessionalGameThrowersTranslation(item):
	'''
	"ProfessionalGameThrower's Translation"
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractProxyTranslations(item):
	'''
	'Proxy Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractRaenadelTranslations(item):
	'''
	'Raenadel Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractRefreshTranslations(item):
	'''
	'Refresh Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractRokudenashiTranslations(item):
	'''
	'rokudenashi Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractRozenFantasyTranslations(item):
	'''
	'Rozen Fantasy Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractSarahslilNovelsCorner(item):
	'''
	"Sarah's lil Novels Corner"
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractSegmetonTranslation(item):
	'''
	'Segmeton Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractSelfishTranslation(item):
	'''
	'Selfish Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractSharramycatsTranslations(item):
	'''
	'Sharramycats Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractSilavinsTranslations(item):
	'''
	"Silavin's Translations"
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractSlothTranslation(item):
	'''
	'Sloth Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractSnailsPace(item):
	'''
	"Snail's Pace"
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractSpaceforMemory(item):
	'''
	'SpaceforMemory'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractStrayCats(item):
	'''
	'StrayCats'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractSuperNyankoMofu(item):
	'''
	'SuperNyankoMofu~'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractTheOtherHalfofMyApple(item):
	'''
	'The Other Half of My Apple'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractTheWorldOnTheOtherSide(item):
	'''
	'The World On The Other Side…'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractTowardstheSky(item):
	'''
	'Towards the Sky'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractTranslatingSloth(item):
	'''
	'Translating Sloth'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractTtukkirabitTranslation(item):
	'''
	'Ttukkirabit Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractUnicornsGalore(item):
	'''
	'UnicornsGalore!'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractVersatileGuy(item):
	'''
	'Versatile Guy'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractWhiteleafTribe(item):
	'''
	'Whiteleaf Tribe'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractWinterTranslates(item):
	'''
	'Winter Translates'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractWorkingNEETTranslation(item):
	'''
	'Working NEET Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractWorksofKun(item):
	'''
	'Works of Kun'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractWuxiaNation(item):
	'''
	'WuxiaNation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractNepustation(item):
	'''
	'www.nepustation.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractXianForeigners(item):
	'''
	'Xian Foreigners'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractYamtl(item):
	'''
	'yamtl'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractYuanshusCave(item):
	'''
	"Yuanshu's Cave"
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractYuNSTranslations(item):
	'''
	'yuNS Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractZaelumTranslations(item):
	'''
	'Zaelum Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extract不法之徒LawlessGangster(item):
	'''
	'《不法之徒》 Lawless Gangster'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extract愛主の翻訳AinushiTranslations(item):
	'''
	'愛主の翻訳  Ainushi Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


