

import runStatus
runStatus.preloadDicts = False

import WebMirror.OutputFilters.FilterBase

import common.database as db

import WebMirror.OutputFilters.util.MessageConstructors  as msgpackers
from WebMirror.OutputFilters.util.TitleParsers import extractTitle

import sqlalchemy.exc
import bs4
import re
import calendar
import traceback
import datetime
import time
import json
import cssutils

########################################################################################################################
#
#	##     ##    ###    #### ##    ##     ######  ##          ###     ######   ######
#	###   ###   ## ##    ##  ###   ##    ##    ## ##         ## ##   ##    ## ##    ##
#	#### ####  ##   ##   ##  ####  ##    ##       ##        ##   ##  ##       ##
#	## ### ## ##     ##  ##  ## ## ##    ##       ##       ##     ##  ######   ######
#	##     ## #########  ##  ##  ####    ##       ##       #########       ##       ##
#	##     ## ##     ##  ##  ##   ###    ##    ## ##       ##     ## ##    ## ##    ##
#	##     ## ##     ## #### ##    ##     ######  ######## ##     ##  ######   ######
#
########################################################################################################################




class NuBaseFilter(WebMirror.OutputFilters.FilterBase.FilterBase):


	def getMaskedClasses(self, soup):

		masked_classes = []

		mask_style = soup.find_all("style", text=re.compile(r"\.chp\-release\..*?display:none"))
		for style in mask_style:
			parsed_style = cssutils.parseString(style.get_text())
			for rule in parsed_style:
				if rule.type == rule.STYLE_RULE:
					disp = rule.style.getProperty('display')
					if disp and disp.cssValue.cssText.lower() == "none":
						for selector in rule.selectorList:
							if len(selector.seq) == 2:
								root, key = selector.seq
								if root.value == ".chp-release" and root.type == 'class':
									masked_classes.append(key.value[1:])

		print("Masked classes:")
		print(masked_classes)

		return masked_classes
