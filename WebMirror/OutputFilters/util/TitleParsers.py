
#!/usr/bin/python
# from profilehooks import profile
import urllib.parse
import re
import json
import logging
import settings
from WebMirror.util.titleParseNew import TitleParser


from WebMirror.OutputFilters.util.MessageConstructors import buildReleaseMessage

# pylint: disable=W0201


skip_filter = [
	"www.baka-tsuki.org",
	"re-monster.wikia.com",
]

def extractTitle(inStr):
	# print("Parsing: '%s'" % inStr)
	p    = TitleParser(inStr)
	vol  = p.getVolume()
	chp  = p.getChapter()
	frag = p.getFragment()
	post = p.getPostfix()

	if (chp and not frag) or (chp and float(int(float(chp))) != float(chp) and (frag == 0 or frag is None)):
		chp = int(chp)
		frag = int(chp * 100) % 100

	# if chp:
	# 	assert float(int(float(chp))) == float(chp), "chp is not an integer ('%s', %s, %s, %s)! Wat?" % (inStr, vol, chp, frag)
	# if vol:
	# 	assert float(int(float(vol))) == float(vol), "vol is not an integer ('%s', %s, %s, %s)! Wat?" % (inStr, vol, chp, frag)
	# if frag:
	# 	assert float(int(float(frag))) == float(frag), "frag is not an integer ('%s', %s, %s, %s)! Wat?" % (inStr, vol, chp, frag)



	return vol, chp, frag, post

def extractChapterVol(inStr):
	vol, chp, dummy_frag, dummy_post = extractTitle(inStr)
	return chp, vol

def extractVolChapterFragmentPostfix(inStr):
	vol, chp, frag, post = extractTitle(inStr)
	return vol, chp, frag, post

def extractChapterVolFragment(inStr):
	vol, chp, frag, dummy_post = extractTitle(inStr)
	return chp, vol, frag
