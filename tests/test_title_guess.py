
import time
import traceback

# from FeedScrape.FeedDataParser import extractChapterVol
from tests.title_test_data import data as test_data
from WebMirror.OutputFilters.util.TitleParsers import TitleParser

def test():
	count = 0
	mismatch = 0
	start = time.time()
	for key, value in test_data:
		try:
			# if not "  " in key:
			# 	continue

			# print(key, value)
			p = TitleParser(key)
			vol, chp, frag, post = p.getVolume(), p.getChapter(), p.getFragment(), p.getPostfix()

			# if frag != None:
			# 	consolidated_chp = (frag / 100.0) + 0 if chp == None else chp
			# else:
			# 	consolidated_chp = chp
			# if len(value) == 2:
			# 	e_chp, e_vol = value
			# 	if e_chp == 0.0 and consolidated_chp == None:
			# 		e_chp = None
			# 	if vol != e_vol or consolidated_chp != e_chp:
			# 		mismatch += 1
			# 		print(p)
			# 		print("Parsed: v{}, c{}".format(vol, consolidated_chp))
			# 		print("Expect: v{}, c{}".format(e_vol, e_chp))
			# 		print()
			# elif len(value) == 4:
			# 	e_vol, e_chp, e_frag, e_post = value
			# 	if e_chp == 0.0 and chp == None:
			# 		e_chp = None
			# 	if vol != e_vol or chp != e_chp or frag != e_frag:
			# 		mismatch += 1
			# 		print(p)
			# 		print("Parsed: v{}, c{}, f{}".format(vol, chp, frag))
			# 		print("Expect: v{}, c{}, f{}".format(e_vol, e_chp, e_frag))
			# 		print()
			# 	if e_post != post:
			# 		mismatch += 1
			# 		print(p)
			# 		print("Parsed: {}".format(post))
			# 		print("Expect: {}".format(e_post))
			# 	# for number in p.getNumbers():
			# 	# 	print(number)
			# 	# 	print("Preceeded by:", number.lastData())
			count += 1
		except Exception:
			mismatch += 1
			traceback.print_exc()

		# if len(value) == 2:
		# 	assert value == extractChapterVol(key), "Wat? Values: '{}', '{}', '{}'".format(key, value, extractChapterVol(key))
		# elif len(value) == 4:
		# 	assert value == extractVolChapterFragmentPostfix(key), "Wat? Values: '{}', '{}', '{}'".format(key, value, extractVolChapterFragmentPostfix(key))
		# else:
		# 	print("Wat?")
		# 	print(key, value)
	# print("All matches passed!")

	stop = time.time()

	delta = stop - start

	print("Total time: {}, time per title: {}".format(delta, delta / len(test_data)))

	print("{} Items with parsed output".format(count))
	print("{} Items mismatch in new parser".format(mismatch))
	print("Total items: {}".format(len(test_data)))


if __name__ == "__main__":

	test()

