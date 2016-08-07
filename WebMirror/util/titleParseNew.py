
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
		':',
		'"',
		'/',
		'\\',
	]

class NumberConversionException(Exception):
	pass

################################################################################################################################
################################################################################################################################
################################################################################################################################

def intersperse(iterable, delimiter):
	it = iter(iterable)
	yield next(it)
	for x in it:
		yield delimiter
		yield x

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
		return list(intersperse(instr.split(" "), " "))

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
		# print("Splitting: '%s'" % instr)
		for letter in instr:
			if (prev and
					(
							prev in string.digits and letter not in string.digits
						or
							letter in string.digits and prev not in string.digits
						)):

				if prev.lower() == "r":
					# print("Not splitting (1):", letter, prev)
					prev = letter
					agg += letter

				# Don't split on letter-decimal sequences
				elif (
						(prev.lower() in string.digits and letter.lower() == ".")
						or
						(letter.lower() in string.digits and prev.lower() == ".")
						):
					# print("Not splitting (2):", letter, prev)
					prev = letter
					agg += letter
				else:
					if agg:
						ret.append(agg)
						agg = ""
					agg += letter
					# ret.append(letter)
					# print("Splitting, ", letter, prev)
					prev = letter
			else:
				# print("Not splitting (3):", (letter, prev, agg))
				prev = letter
				agg += letter

		# print("End: ", (ret, agg))
		if agg:
			ret.append(agg)
		# print("Split: '%s'" % ret)
		return ret

#############################

################################################################################################################################
################################################################################################################################
################################################################################################################################

class TokenBase(object):
	def __init__(self, prefix, intermediate, content):
		self.prefix       = prefix
		self.intermediate = intermediate
		self.content      = content

	def string(self):
		return self.content

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


		raise NumberConversionException("Failed to convert '%s' to a number!" % (self.content, ))



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
class FreeChapterToken(NumericToken):
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

		# print("get_preceeding_text", (prefix_arr, None, intermediate))
		return [], None, intermediate

	def process(self, inarr):
		# print("Globber processing", inarr)
		assert isinstance(inarr, (list, tuple))
		negoff = 0
		original_length = len(inarr)
		for idx in range(original_length):
			locidx = idx - negoff
			inarr = self.attach_token(inarr[:locidx], inarr[locidx], inarr[locidx+1:])
			negoff = original_length - len(inarr)
			# print("Globber step", inarr)

		# print("Globber return", inarr)
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
			# 'episode'
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

		# print("Getting text preceding '%s' (%s)" % (target, type(target)))

		before, prec, intervening = self.get_preceeding_text(before)

		if target == " ":
			if prec:
				before.append(prec)
			if intervening:
				before.append(intervening)
		else:
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

		# print((before, prec, intervening, target, after))

		ret = before
		if target:
			ret = ret + [target]
		if len(after):
			ret = ret + after

		# print("Returning:   ", ret)
		# print()
		return ret

class FreeNumericChapterGlobber(GlobBase):

	def attach_token(self, before, target, after):
		# print("Attach FreeNumericChapterGlobber: ", target)
		if isinstance(target, str):
			tmp = FreeChapterToken('', '', target)
			if tmp.is_valid(parse_ascii=False):
				# print("Interpreting as FreeChapterToken: ", target)
				target = tmp

		# print((before, prec, intervening, target, after))

		ret = before + [target]
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
		FreeNumericChapterGlobber,
		FreeTextGlobber,
	]

	def __init__(self, title):
		self.raw = title

		self.chunks = []

		# print()
		# print()
		# print()
		# print("Parsing title: '%s'" % title)

		for splitter in self.SPLITTERS:
			title = splitter().process(title)
			# print("Splitter step: ", title)

		for globber in self.INTERPRETERS:
			title = globber().process(title)
			# print("Globber step: ", title)

		self.chunks = title

	def __getitem__(self, idx):
		return self.chunks[idx]

	def getTok(self, tok_cls, do_print=False):

		for do_ascii in [False, True]:
			for item in self.chunks:
				# if do_print:
				# 	print(item, tok_cls, isinstance(item, tok_cls))
				if isinstance(item, tok_cls):
					if item.is_valid(parse_ascii=do_ascii):
						return item.to_number(parse_ascii=do_ascii)
		return None





	def getVolume(self):
		return self.getTok(VolumeToken)

	def getChapter(self):
		types = [ChapterToken, FreeChapterToken]
		for toktype in types:
			norm = self.getTok(toktype)
			# print("Tok:", toktype, norm)
			if norm is not None:
				# print("returning:", norm)
				return norm
		return None

	def getFragment(self):
		return self.getTok(FragmentTokenToken)


	def _splitPostfix(self, inStr):


		return inStr.strip()

	def getPostfix(self):

		for idx in range(len(self.chunks)):
			# Do not glob onto postfixes untill there are no
			# attached chapter/volume items remaining.
			# Specifically, we allow fragment or free chapter tokens,
			# because they can unintentionally attach to postfix numbering.
			if any([isinstance(chunk, (VolumeToken, ChapterToken, FragmentTokenToken)) for chunk in self.chunks[idx:]]):
				continue

			for p_key in POSTFIX_KEYS:
				if len(p_key) == 1:
					if p_key[0] in self.chunks[idx].string().lower():
						ret = ''.join([chunk.string() for chunk in self.chunks[idx:]])
						return self._splitPostfix(ret)
				if len(p_key) == 2:
					if (
								p_key[0] in self.chunks[idx].string().lower()
							and
								len(self.chunks) > (idx + 1)
							and
								p_key[1] in self.chunks[idx+1].string().lower()
						):
						ret = ''.join([chunk.string() for chunk in self.chunks[idx:]])
						return self._splitPostfix(ret)
		return ''

	def __repr__(self):
		ret = "<Parsed title: '{}' v:{}, c:{}, f:{}\n".format(self.raw, self.getVolume(), self.getChapter(), self.getFragment())
		for item in self.chunks:
			ret += "	{}\n".format(item)
		ret += ">"
		ret = ret.strip()
		return ret

