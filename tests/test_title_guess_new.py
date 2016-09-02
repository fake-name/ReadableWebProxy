
# from FeedScrape.FeedDataParser import extractChapterVol
from WebMirror.util.titleParseNew import TitleParser as TPN
from WebMirror.util.titleParse import TitleParser as TP

import common.database as db

def test():
	from tests.title_test_data import data as test_data
	# from tests.title_test_data_two import data as test_data_more
	count = 0
	mismatch = 0
	for key, value in test_data:
		# if not "  " in key:
		# 	continue

		# print(key, value)
		p = TPN(key)
		vol, chp, frag, post = p.getVolume(), p.getChapter(), p.getFragment(), p.getPostfix()

		# print(p)

		if len(value) == 2:
			pass
		elif len(value) == 4:
			e_vol, e_chp, e_frag, e_post = value
			if e_chp == 0.0 and chp is None:
				e_chp = None

			bad = False
			if vol != e_vol or chp != e_chp or frag != e_frag:
				bad = True
				print(p)
				print("Parsed: v{}, c{}, f{}".format(vol, chp, frag))
				print("Expect: v{}, c{}, f{}".format(e_vol, e_chp, e_frag))
				print()

			if e_post != post:
				bad = True
				print(p)
				print("Post mismatch - Parsed: {}".format(post))
				print("Post mismatch - Expect: {}".format(e_post))

			if bad:
				mismatch += 1

			# elif post:
			# 	print("Valid post - Parsed: {}".format(post))


			# for number in p.getNumbers():
			# 	print(number)
			# 	print("Preceeded by:", number.lastData())
		count += 1

		# if len(value) == 2:
		# 	assert value == extractChapterVol(key), "Wat? Values: '{}', '{}', '{}'".format(key, value, extractChapterVol(key))
		# elif len(value) == 4:
		# 	assert value == extractVolChapterFragmentPostfix(key), "Wat? Values: '{}', '{}', '{}'".format(key, value, extractVolChapterFragmentPostfix(key))
		# else:
		# 	print("Wat?")
		# 	print(key, value)

	# print("All matches passed!")
	print("{} Items with parsed output".format(count))
	print("{} Items mismatch in new parser".format(mismatch))
	print("Total items: {}".format(len(test_data)))

def extract_mismatch():
	from tests.title_test_data import data as test_data
	from tests.title_test_data_two import data as test_data_more
	count = 0
	mismatch = 0

	test_data_dict = {}
	for key, value in test_data_more:
		if not key in test_data_dict:
			test_data_dict[key] = []
		test_data_dict[key].append(value)
	for key, value in test_data:
		test_data_dict[key] = []
	for key, value in test_data:
		test_data_dict[key].append(value)

	with open("tests/title_test_data_mismatch.py", 'w') as fp:
		fp.write("data = [\n")
		goodstr = []
		badstr = []
		errored = []
		for key, value in test_data_dict.items():
			try:
				p = TPN(key)
				vol, chp, frag, post = p.getVolume(), p.getChapter(), p.getFragment(), p.getPostfix()
				# print(p)
				badtmp = ''
				goodtmp = ''
				for valueset in value:
					assert (len(valueset) == 4), "Wat: %s" % (valueset, )
					e_vol, e_chp, e_frag, e_post = valueset

					if e_chp == 0.0 and chp is None:
						e_chp = None

					bad = False
					if vol != e_vol or chp != e_chp or frag != e_frag:
						bad = True
						print(p)
						print("Parsed: v{}, c{}, f{}".format(vol, chp, frag))
						print("Expect: v{}, c{}, f{}".format(e_vol, e_chp, e_frag))
						print()

					if e_post != post:
						bad = True
						print(p)
						print("Post mismatch - Parsed: {}".format(post))
						print("Post mismatch - Expect: {}".format(e_post))

					if bad:
						mismatch += 1


					if vol != e_vol or chp != e_chp or frag != e_frag or e_post != post:
						badtmp = format_row(key, e_vol, e_chp, e_frag, e_post)
					else:
						goodtmp = format_row(key, e_vol, e_chp, e_frag, e_post)

				if goodtmp:
					goodstr.append(goodtmp)
				else:
					badstr.append(badtmp)
			except AssertionError:
				errored.append(format_row(key, None, None, None, ''))

			count += 1
		goodstr.sort()
		badstr.sort()

		fp.write("".join(goodstr))
		fp.write("\n\n")
		fp.write("#################################################################################################################################################################################################################################")
		fp.write("#################################################################################################################################################################################################################################")
		fp.write("#################################################################################################################################################################################################################################")
		fp.write("#################################################################################################################################################################################################################################")
		fp.write("\n\n")
		fp.write("".join(badstr))
		fp.write("\n\n")
		fp.write("#################################################################################################################################################################################################################################")
		fp.write("#################################################################################################################################################################################################################################")
		fp.write("#################################################################################################################################################################################################################################")
		fp.write("#################################################################################################################################################################################################################################")
		fp.write("\n\n")
		fp.write("".join(errored))

		fp.write("]\n")

	# print("All matches passed!")
	print("{} Items with parsed output".format(count))
	print("{} Items mismatch in new parser".format(mismatch))
	print("{} error encountered in parsing".format(len(errored)))
	print("Total items: {}".format(len(test_data)))

def test_mismatch():
	from tests.title_test_data_mismatch import data as test_data
	count = 0
	mismatch = 0

	for key, value in test_data:

		p = TPN(key)
		vol, chp, frag, post = p.getVolume(), p.getChapter(), p.getFragment(), p.getPostfix()

		# print(p)
		if len(value) == 4:
			e_vol, e_chp, e_frag, e_post = value

			if e_chp == 0.0 and chp is None:
				e_chp = None
			bad = False
			if vol != e_vol or chp != e_chp or frag != e_frag:
				bad = True
				print(p)
				print("Parsed: v{}, c{}, f{}".format(vol, chp, frag))
				print("Expect: v{}, c{}, f{}".format(e_vol, e_chp, e_frag))
				print()

			if e_post != post:
				bad = True
				print(p)
				print("Post mismatch - Parsed: {}".format(post))
				print("Post mismatch - Expect: {}".format(e_post))

			if bad:
				mismatch += 1

		count += 1


	# print("All matches passed!")
	print("{} Items with parsed output".format(count))
	print("{} Items mismatch in new parser".format(mismatch))
	print("Total items: {}".format(len(test_data)))

def format_row(title, volume, chapter, fragment, postfix):
	return "	" + str((title, (volume, chapter, fragment, postfix))) + ",\n"

def load_items():
	feed_items = db.get_db_session().query(db.FeedItems) \
			.order_by(db.FeedItems.srcname)           \
			.order_by(db.FeedItems.title)           \
			.all()

	with open("tests/title_test_data_two.py", 'w') as fp:
		fp.write("data = [\n")
		for row in feed_items:
			title = row.title

			try:
				p = TP(title)
				fp.write(format_row(title, p.getVolume(), p.getChapter(), p.getFragment(), p.getPostfix()))
			except ValueError:
				fp.write(format_row(title, 0, 0, 0, ''))

		fp.write("]\n")

if __name__ == "__main__":
	import sys
	if 'regenerate' in sys.argv:
		load_items()
	elif "extract-mismatch" in sys.argv:
		extract_mismatch()
	elif "test-mismatch" in sys.argv:
		test_mismatch()
	else:
		test()

