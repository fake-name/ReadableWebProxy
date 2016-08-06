
import abc
import string
import semantic.numbers
import traceback

POSTFIX_KEYS = [
		['prologue'],
		['afterword'],
		['epilogue'],
		['interlude'],
		['foreword'],
		['appendix'],
		['intermission'],
		['sidestory'],
		['side', 'story'],
		['extra'],
		['illustrations'],
	]

POSTFIX_SPLITS = [
		'-',
		'–',  # FUCK YOU UNICODE
		':',
	]

# Additional split characters
SPLIT_ON = [
		"!",
		")",
		"(",
		"[",
		"]",

		# Fucking quotes
		'"',
		'/',
		'\\',
	]

class NumberConversionException(Exception):
	pass

################################################################################################################################
################################################################################################################################
################################################################################################################################

class SplitterBase(object):
	__metaclass__ = abc.ABCMeta

	def process(self, inarr):
		if isinstance(inarr, str):
			tmp = self.split_component(inarr)
			assert isinstance(tmp, (list, tuple))
			return tmp
		elif isinstance(inarr, (list, tuple)):
			ret = []
			for chunk in inarr:
				tmp = self.split_component(chunk)
				assert isinstance(tmp, (list, tuple))
				[ret.append(subcmp) for subcmp in tmp]
			return ret

	@abc.abstractmethod
	def split_component(self, instr):
		pass

class SpaceSplitter(SplitterBase):
	def split_component(self, instr):
		return instr.split(" ")

class CharSplitter(SplitterBase):
	def split_component(self, instr):
		ret = []
		agg = ""
		for letter in instr:
			if letter in SPLIT_ON:
				if agg:
					ret.append(agg)
					agg = ""
				ret.append(letter)
			else:
				agg += letter
		if agg:
			ret.append(agg)

		return ret


class LetterNumberSplitter(SplitterBase):
	def split_component(self, instr):
		ret = []
		agg = ""
		prev = None
		for letter in instr:
			if (prev and
					(
							prev in string.digits and letter not in string.digits and letter not in ['.-']
						or
							letter in string.digits and prev not in string.digits and prev not in ['.-']
						)):
				if agg:
					ret.append(agg)
					agg = ""
				ret.append(letter)
				prev = letter
			else:
				prev = letter
				agg += letter
		if agg:
			ret.append(agg)

		return ret

################################################################################################################################
################################################################################################################################
################################################################################################################################

class TokenBase(object):
	def __init__(self, prefix, intermediate, content):
		self.prefix       = prefix
		self.intermediate = intermediate
		self.content      = content

	def __repr__(self):
		# print("Token __repr__ call!")
		ret = "<{:14} - contents: '{}' '{}' '{}'>".format(self.__class__.__name__, self.prefix, self.intermediate, self.content)
		return ret


class FreeTextToken(TokenBase):
	def __init__(self, content):
		self.content      = content

	def __repr__(self):
		# print("Token __repr__ call!")
		ret = "<{:14} - contents: '{}'>".format(self.__class__.__name__, self.content)
		return ret

class NumericToken(TokenBase):

	def __repr__(self):
		# print("Token __repr__ call!")
		ret = "<{:14} - contents: '{}' '{}' '{}' (numeric: {}, ascii: {}, parsed: {}>".format(self.__class__.__name__,
			self.prefix, self.intermediate, self.content,
			self.is_valid(parse_ascii=False), self.is_valid(parse_ascii=True) and not self.is_valid(parse_ascii=False),
			self.to_number(parse_ascii=True) if self.is_valid(parse_ascii=True) else 'No'
			)
		return ret

	def to_number(self, parse_ascii):

		if not self.content:
			raise NumberConversionException("Failed to convert '%s' to a number!" % (self.content, ))
		# Handle strings with multiple decimal points, e.g. '01.05.15'
		if self.content.count(".") > 1:
			raise NumberConversionException("Failed to convert '%s' to a number! Too many decimal points" % (self.content, ))

		# NumberService() for some reason converts "a" to "one", which fucks everything up.
		# Anyways, if the token is "a", stop it from doing that.
		if self.content.strip().lower() == 'a':
			raise NumberConversionException("Failed to convert '%s' to a number!" % (self.content, ))

		# Make sure we have at least one digit
		if not parse_ascii and not any([char in '0123456789' for char in self.content]):
			raise NumberConversionException("Failed to convert '%s' to a number! No numbers, and not trying to parse ascii numbers" % (self.content, ))

		if all([char in '0123456789.' for char in self.content]):
			return float(self.content)

		if parse_ascii:
			# return float(self.content)
			val = self.ascii_numeric()
			# print("Ascii_numeric call return: ", val)
			if val != False:
				return val

			raise NumberConversionException("Call assumes '%s' is numeric, and it's not." % (self.content))
			# assert self.is_valid(), "getNumber() can only be called if the token value is entirely numeric!"


		return False



	def is_valid(self, parse_ascii):
		'''
		Does the token contain a value that could (probably) be
		converted to an integer without issue.

		TODO: just use try float(x)?
		'''

		try:
			self.to_number(parse_ascii)
			return True
		except NumberConversionException:
			return False


	def ascii_numeric(self):


		content = self.content

		bad_chars = [":", ";", ",", "[", "]"]
		for bad_char in bad_chars:
			if bad_char in content:
				content = content.split(bad_char)[0]

		# text-to-number library does stupid things with "a" or "A" (converts them to 1)
		content = content.split(" ")
		if "a" in content: content.remove("a")
		if "A" in content: content.remove("A")
		content = " ".join(content)


		# Spot-patching to fix data corruption issues I've run into:

		content = content.replace("”", "")
		content = content.strip()
		# print("AsciiNumeric concatenated string: '%s'" % content)
		while content:
			try:
				# print("Parsing '%s' for numbers" % content)
				ret = semantic.numbers.NumberService().parse(content)
				# print("parsed: ", ret)
				# print(traceback.print_stack())
				return ret
			except semantic.numbers.NumberService.NumberException:
				# print("Failed to parse: ", content)
				try:
					# Try again with any trailing hyphens removed
					# semantic assumes "twenty-four" should parse as "twenty four".
					# this is problematic when you have "chapter one - Thingies", which
					# tries to parse as "one - thingies", and fails.
					# However, we only want to invoke this fallback if
					# we can't parse /with/ the hyphen, as lots of sources actually do release
					# as "twenty-four"
					if "-" in content:
						content = content.split("-")[0].strip()
						val = semantic.numbers.NumberService().parse(content)
						return val

					# It also mangles trailing parenthesis, for some reason.
					if ")" in content or "(" in content:
						content = content.split(")")[0].split("(")[0].strip()
						val = semantic.numbers.NumberService().parse(content)
						return val


				except semantic.numbers.NumberService.NumberException:
					pass

				# print("Parse failure!")
				# traceback.print_exc()
				if not " " in content:
					# print("Parse failure?")
					return False
				content = content.rsplit(" ", 1)[0]
		# print("Parse reached end of buffer without content")
		return False



class VolumeToken(NumericToken):
	pass
class ChapterToken(NumericToken):
	pass
class FragmentTokenToken(NumericToken):
	pass

################################################################################################################################
################################################################################################################################
################################################################################################################################


# !?^%!$,
# !?^%!$,!

# class Token(object):
class GlobBase(object):
	__metaclass__ = abc.ABCMeta

	def get_preceeding_text(self, prefix_arr):
		intermediate = ""
		consumed = 0

		for idx in range(len(prefix_arr)-1, 0-1, -1):
			if isinstance(prefix_arr[idx], TokenBase):
				return prefix_arr, None, intermediate
			if all([char in string.punctuation+string.whitespace for char in prefix_arr[idx]]):
				intermediate = prefix_arr[idx] + intermediate
				consumed += 1
			else:
				return prefix_arr[:idx], prefix_arr[idx], intermediate

		return prefix_arr, None, intermediate

	def process(self, inarr):
		assert isinstance(inarr, (list, tuple))
		negoff = 0
		original_length = len(inarr)
		for idx in range(original_length):
			locidx = idx - negoff
			inarr = self.attach_token(inarr[:locidx], inarr[locidx], inarr[locidx+1:])
			negoff = original_length - len(inarr)

		return inarr

	@abc.abstractmethod
	def attach_token(self, before, target, after):
		return None


class VolumeChapterFragGlobber(GlobBase):

	# Order matters! Items are checked from left to right.
	VOLUME_KEYS   = [
			'volume',
			'season',
			'book',
			'vol',
			'vol.',
			'arc',
			'v',
			'b',
			's',

			# Spot fixes: Make certain scanlators work:
			'rokujouma',
			'sunlight',
		]


	FRAGMENT_KEYS = [
			'part',
			'episode',
			'pt',
			'part',
			'parts',
			'page',
			'p',
			'pt.',

			# Handle chapter sequences /somewhat/ elegantly
			# e.g. chp 1-3
			# That's either chapter 1 through 3, or
			# chapter 1 part 3.
			# In any event, the first is harmless, and the
			# latter is better then before, so.... eh?
			'-'
		]
	CHAPTER_KEYS  = [
			'chapter',
			'ch',
			'c',
			'episode'
		]

	# Do NOT glob onto numeric values preceeded by "r",
	# so "(R18) Title Blah 4" doesn't get universally interpreted
	# as chapter 18.
	CHAPTER_NUMBER_NEGATIVE_MASKS = [
		"r",
	]

	glob_ascii = False

	def attach_token(self, before, target, after):
		# print("AttachToken: ", (before, target, after))
		# if len(after) == 3:
		# 	target = before[-1] + target
		# 	before = before[:-1]

		# print("Getting text preceding '%s'" % target)
		before, prec, intervening = self.get_preceeding_text(before)
		if prec and prec.lower() in self.VOLUME_KEYS:
			target = VolumeToken(prec, intervening, target)
		elif prec and prec.lower() in self.CHAPTER_KEYS:
			target = ChapterToken(prec, intervening, target)
		elif prec and prec.lower() in self.FRAGMENT_KEYS:
			target = FragmentTokenToken(prec, intervening, target)

		else:
			if prec:
				before.append(prec)
			if intervening:
				before.append(intervening)


		ret = before
		if target:
			ret = ret + [target]
		if len(after):
			ret = ret + after
		return ret

class FreeTextGlobber(GlobBase):

	def attach_token(self, before, target, after):
		if isinstance(target, str):
			target = FreeTextToken(target)

		ret = before
		if target:
			ret = ret + [target]
		if len(after):
			ret = ret + after
		return ret

		# print("AttachToken: ", (before, target, after))
		# if len(after) == 3:
		# 	target = before[-1] + target
		# 	before = before[:-1]
	# FreeTextToken


################################################################################################################################
################################################################################################################################
################################################################################################################################

class TitleParser(object):

	SPLITTERS = [
		SpaceSplitter,
		CharSplitter,
		LetterNumberSplitter,
	]

	INTERPRETERS = [
		VolumeChapterFragGlobber,
		FreeTextGlobber,
	]

	def __init__(self, title):
		self.raw = title

		self.chunks = []
		indice = 0
		data = ''

		print()
		print()
		print()
		print("Parsing title: '%s'" % title)

		for splitter in self.SPLITTERS:
			title = splitter().process(title)

		for globber in self.INTERPRETERS:
			title = globber().process(title)


		self.chunks = title
		# # Consume the string.
		# while indice < len(self.raw):
		# 	delimiter = getDelimiter(self.raw[indice:], self.DELIMITERS)
		# 	if delimiter:
		# 		assert self.raw[indice:].startswith(delimiter)
		# 		if data:
		# 			self.appendDataChunk(data)
		# 			data = ''
		# 		self.appendDelimiterChunk(self.raw[indice:indice+len(delimiter)])
		# 		indice = indice+len(delimiter)
		# 	else:
		# 		data += self.raw[indice]
		# 		indice += 1

		# # Finally, tack on any trailing data tokens (if they're present)
		# if data:
		# 	self.appendDataChunk(data)

	def __getitem__(self, idx):
		return self.chunks[idx]

	def appendDelimiterChunk(self, rawdat):
		tok  = DelimiterToken(
			text     = rawdat,
			position = len(self.chunks),
			parent   = self)
		self.chunks.append(tok)

	def appendDataChunk(self, rawdat):

		d_tok = DataToken(
				text     = rawdat,
				position = len(self.chunks),
				parent   = self)
		d_toks = d_tok.splitToken(DataToken)
		for tok in d_toks:
			tok = tok.specialize(self.SPECIALIZE, self.ASCII_SPECIALIZE)
			self.chunks.append(tok)

	def _preceeding(self, offset):
		return [chunk for chunk in self.chunks[:offset] if not isinstance(chunk, (DelimiterToken, NullToken))]

	def _following(self, offset):
		return [chunk for chunk in self.chunks[offset+1:] if not isinstance(chunk, (DelimiterToken, NullToken))]

	def _following_text(self, offset):
		chunks = [chunk for chunk in self.chunks[offset+1:] if not any([isinstance(chunk, ttype) for ttype in self.SPECIALIZE])]
		texts = [chunk.text for chunk in chunks]
		return "".join(texts)

	def _getTokenType(self, tok_type):
		return [chunk for chunk in self.chunks if isinstance(chunk, tok_type)]


	def getNumbers(self):
		return [item for item in self.chunks if item.isNumeric()]

	def getVolumeItem(self):
		# have = self._getTokenType(VolumeToken)
		# if have:
		# 	return have[0]
		return None

	def getVolume(self):
		# have = self.getVolumeItem()
		# if not have:
		# 	return None
		# return have.getNumber()
		return None

	def getFragment(self):
		# have = self._getTokenType(FragmentToken)
		# if have:
		# 	return have[0].getNumber()
		return None


	def _splitPostfix(self, inStr):
		# for key in POSTFIX_SPLITS:
		# 	print(key, key in inStr)
		# 	if key in inStr:
		# 		return inStr.split(key, 1)[-1]


		return inStr.strip()

	def getPostfix(self):

		# for idx in range(len(self.chunks)):
		# 	s_tmp = self.chunks[idx].stringl()
		# 	# Do not glob onto postfixes untill there are no
		# 	# attached chapter/volume items remaining.
		# 	# Specifically, we allow fragment or free chapter tokens,
		# 	# because they can unintentionally attach to postfix numbering.
		# 	if any([isinstance(chunk, (VolumeToken, ChapterToken)) for chunk in self._following(idx)]):
		# 		continue

		# 	for p_key in POSTFIX_KEYS:
		# 		if len(p_key) == 1:
		# 			if p_key[0] in s_tmp:
		# 				ret = ''.join([chunk.string() for chunk in self.chunks[idx:]])
		# 				return self._splitPostfix(ret)
		# 		if len(p_key) == 2:
		# 			if p_key[1] in s_tmp:
		# 				if idx > 0:
		# 					last = self._preceeding(idx)[-1]
		# 				else:
		# 					last = NullToken()
		# 				if p_key[0] in last.stringl():
		# 					ret = ''.join([chunk.string() for chunk in self.chunks[last.index():]])
		# 					return self._splitPostfix(ret)
		return ''

	def getChapterItem(self):
		# Preferentially select proper chapter tokens, rather
		# then free-floating tokens.
		# That way, titles like: '100 Years of Martial Arts – Chapter 2 Finished (╯°□°）╯︵ ┻━┻)'
		# don't unintentionally glob onto '100', when we want it to
		# # select '2' first
		# have = self._getTokenType(ChapterToken)
		# # print("Have chapter:", have)
		# if have:
		# 	return have[0]
		# have = self._getTokenType(FreeChapterToken)
		# if have:
		# 	return have[0]

		return None

	def getChapter(self):
		# # print("GetChapter call")
		# have = self.getChapterItem()
		# # print("GetChapter return: '%s'" % have)
		# if not have:
		# 	return None
		# return have.getNumber()
		return None

	def __repr__(self):
		ret = "<Parsed title: '{}'\n".format(self.raw)
		for item in self.chunks:
			ret += "	{}\n".format(item)
		ret += ">"
		ret = ret.strip()
		return ret

