
import abc

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

		# Spot fixes: Make certain scanlators work:
		'rokujouma',
		'sunlight',
	]


FRAGMENT_KEYS = [
		'part',
		'episode',
		'pt',
		'part',
		'page',
		'p',

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
		"]"
	]


def getDelimiter(instr, delimiters):
	for delimiter in delimiters:
		if instr.startswith(delimiter):
			return delimiter
	return False

def partition(alist, indices):
	return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]

class Token(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def tokens(self):
		pass

	def __init__(self, text, position, parent):
		self.text     = text
		self.position = position
		self.parent   = parent

	def splitToken(self, toktype):
		'''
		split the current token into a list of `toktype` tokens
		on SPLIT_ON characters if they are present in
		the token strin

		Then, split that list of tokens on numeric/non-numeric
		bounds

		Returns a flattened list of tokens. E.g:
		'ch10!'
		becomes :
		['ch10', '!']
		and then:
		['ch', '10', '!']
		Where each instance is a token of type `toktype` containing the
		shown text.
		'''

		idx = 0
		splits = []
		while idx < len(self.text):
			sp = getDelimiter(self.text[idx:], SPLIT_ON)
			if sp:
				splits.append(idx)
				splits.append(idx+len(sp))
				idx = idx+len(sp)
			else:
				idx += 1

		if 0 in splits:
			splits.remove(0)
		if len(self.text) in splits:
			splits.remove(len(self.text))
		if splits:
			ret = []
			offset = 0
			for chunk in partition(self.text, splits):
				ret.append(toktype(chunk, self.position+offset, self.parent))
				offset += 1
		else:
			ret = [self]

		num_ret = []
		for tok in ret:
			tmp = tok.splitNumeric(toktype)
			for val in tmp:
				num_ret.append(val)


		return num_ret

	def splitNumeric(self, toktype):
		'''
		Given a token containing a string that is partially numeric,
		split the token into sub-tokens that break at the numeric/non-numeric boundaries.
		E.g. 'ch03' becomes ['ch', '03']

		Has some internal protections. Does not split on back/forward slashes unless they are the
		first character.

		Returns a list of tokens in all cases. If no splits were done, the list contains
		only `self`. This allows unconditional use of the return value

		'''
		if not any([char in '0123456789' for char in self.text]):
			return [self]
		if ("/" in self.text and self.text.index("/") > 0) or ("\\" in self.text and self.text.index("\\") > 0):
			return [self]

		nmx = self.text[0] in '0123456789.'
		splits = []
		for idx in range(len(self.text)):
			c_nmx = self.text[idx] in '0123456789.'
			if c_nmx != nmx:
				splits.append(idx)
			nmx = c_nmx

		ret = [self]

		offset = 0
		if splits:
			ret = []
			for chunk in partition(self.text, splits):
				ret.append(toktype(chunk, self.position+offset, self.parent))
				offset += 1

		return ret

	def isNumeric(self):
		'''
		Does the token contain a value that could (probably) be
		converted to an integer without issue.

		TODO: just use try float(x)?
		'''
		if not self.text:
			return False
		# Handle strings with multiple decimal points, e.g. '01.05.15'
		if self.text.count(".") > 1:
			return False
		if not any([char in '0123456789' for char in self.text]):
			return False
		if all([char in '0123456789.' for char in self.text]):
			return True
		return False

	def getNumber(self):
		assert self.isNumeric(), "getNumber() can only be called if the token value is entirely numeric!"
		return float(self.text)

	def __repr__(self):
		ret = "<{:14} at: {:2} contents: '{}' number: {}>".format(self.__class__.__name__, self.position, self.text, self.isNumeric())
		return ret

	def index(self):
		return self.position
	def string(self):
		return self.text
	def stringl(self):
		return self.text.lower()

	def lastData(self):
		ret = self.parent._preceeding(self.position)
		if not len(ret):
			return NullToken()
		return ret[-1]

	def nextData(self):
		ret = self.parent._following(self.position)
		if not len(ret):
			return NullToken()
		return ret[0]

	@classmethod
	def wantsToSpecialize(cls, text):
		'''
		Does token type want to specialize on the text
		`text`? Overridden in `FreeChapterToken` token
		type to allow special behaviour.
		'''
		return text in cls.tokens

	def specialize(self, specializations):
		if not self.isNumeric():
			return self

		prev_dat = self.lastData()
		for spec in [spec for spec in specializations]:
			if not self.parent._getTokenType(spec):
				if spec.wantsToSpecialize(prev_dat.stringl()):
					return spec(self.text, self.position, self.parent)
		return self


class DataToken(Token):
	tokens = None

class VolumeToken(Token):
	tokens = VOLUME_KEYS
class ChapterToken(Token):
	tokens = CHAPTER_KEYS
class FragmentToken(Token):
	tokens = FRAGMENT_KEYS

class FreeChapterToken(Token):
	tokens = False

	@classmethod
	def wantsToSpecialize(cls, text):
		'''
		Glob onto any numeric value that is NOT preceeded by
		any of the existing glob lists.
		'''
		return text not in VOLUME_KEYS+CHAPTER_KEYS+FRAGMENT_KEYS

class DelimiterToken(Token):
	tokens = None

class NullToken(Token):
	tokens = None
	text = 'NONE - lolercasterlwklsajhafglkjhasdflkjh'
	def __init__(self):
		pass

	def isNumeric(self):
		return False

	def getNumber(self):
		raise ValueError("NullToken cannot be converted to a number!")

	def __repr__(self):
		ret = "<{:14}>".format(self.__class__.__name__)
		return ret

	def string(self):
		return ''





class TitleParser(object):
	DELIMITERS = [' ', '_', ',', ':', '-']

	# Possible token specializations.
	# Order is important! Options are checked in passed order.
	# Earlier types will preempt globbing by later types
	SPECIALIZE = [
			VolumeToken,
			ChapterToken,
			FragmentToken,
			FreeChapterToken,
		]

	def __init__(self, title):
		self.raw = title

		self.chunks = []
		indice = 0
		data = ''

		# Consume the string.
		while indice < len(self.raw):
			delimiter = getDelimiter(self.raw[indice:], self.DELIMITERS)
			if delimiter:
				assert self.raw[indice:].startswith(delimiter)
				if data:
					self.appendDataChunk(data)
					data = ''
				self.appendDelimiterChunk(self.raw[indice:indice+len(delimiter)])
				indice = indice+len(delimiter)
			else:
				data += self.raw[indice]
				indice += 1

		# Finally, tack on any trailing data tokens (if they're present)
		if data:
			self.appendDataChunk(data)

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
			tok = tok.specialize(self.SPECIALIZE)
			self.chunks.append(tok)

	def _preceeding(self, offset):
		return [chunk for chunk in self.chunks[:offset] if not isinstance(chunk, (DelimiterToken, NullToken))]

	def _following(self, offset):
		return [chunk for chunk in self.chunks[offset+1:] if not isinstance(chunk, (DelimiterToken, NullToken))]

	def _getTokenType(self, tok_type):
		return [chunk for chunk in self.chunks if isinstance(chunk, tok_type)]


	def getNumbers(self):
		return [item for item in self.chunks if item.isNumeric()]

	def getVolumeItem(self):
		have = self._getTokenType(VolumeToken)
		if have:
			return have[0]
		return None

	def getVolume(self):
		have = self.getVolumeItem()
		if not have:
			return None
		return have.getNumber()

	def getFragment(self):
		have = self._getTokenType(FragmentToken)
		if have:
			return have[0].getNumber()
		return None


	def _splitPostfix(self, inStr):
		# for key in POSTFIX_SPLITS:
		# 	print(key, key in inStr)
		# 	if key in inStr:
		# 		return inStr.split(key, 1)[-1]


		return inStr.strip()

	def getPostfix(self):

		for idx in range(len(self.chunks)):
			s_tmp = self.chunks[idx].stringl()
			# Do not glob onto postfixes untill there are no
			# attached chapter/volume items remaining.
			# Specifically, we allow fragment or free chapter tokens,
			# because they can unintentionally attach to postfix numbering.
			if any([isinstance(chunk, (VolumeToken, ChapterToken)) for chunk in self._following(idx)]):
				continue

			for p_key in POSTFIX_KEYS:
				if len(p_key) == 1:
					if p_key[0] in s_tmp:
						ret = ''.join([chunk.string() for chunk in self.chunks[idx:]])
						return self._splitPostfix(ret)
				if len(p_key) == 2:
					if p_key[1] in s_tmp:
						if idx > 0:
							last = self._preceeding(idx)[-1]
						else:
							last = NullToken()
						if p_key[0] in last.stringl():
							ret = ''.join([chunk.string() for chunk in self.chunks[last.index():]])
							return self._splitPostfix(ret)
		return ''

	def getChapterItem(self):
		# Preferentially select proper chapter tokens, rather
		# then free-floating tokens.
		# That way, titles like: '100 Years of Martial Arts – Chapter 2 Finished (╯°□°）╯︵ ┻━┻)'
		# don't unintentionally glob onto '100', when we want it to
		# select '2' first
		have = self._getTokenType(ChapterToken)
		if have:
			return have[0]
		have = self._getTokenType(FreeChapterToken)
		if have:
			return have[0]

		return None

	def getChapter(self):
		have = self.getChapterItem()
		if not have:
			return None
		return have.getNumber()

	def __repr__(self):
		ret = "<Parsed title: '{}'\n".format(self.raw)
		for item in self.chunks:
			ret += "	{}\n".format(item)
		ret += ">"
		ret = ret.strip()
		return ret

