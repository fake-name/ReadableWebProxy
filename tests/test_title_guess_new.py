
import ast
import os
import os.path
import pprint
import tqdm
import traceback

# from FeedScrape.FeedDataParser import extractChapterVol
from WebMirror.util.titleParseNew import TitleParser as TPN

import common.database as db


def load_better_json(filepath):
	'''
	Load a json file, but allow shit necessary for sanity (like comments!)
	'''

	print("Loading file: '%s'" % filepath)
	with open(filepath) as fp:
		contin = fp.read()

	return ast.literal_eval(contin)


def load_test_data(mismatch=True, only_mismatch=False):
	ret = []
	cdir = os.path.join(os.path.dirname(__file__), "title_data")
	files = os.listdir(cdir)
	files.sort()
	for fn in files:

		if fn.endswith(".pyson"):
			fqp = os.path.join(cdir, fn)

			if only_mismatch:
				if "mismatch" in fn:
					ret.extend(load_better_json(fqp))
			elif mismatch:
				ret.extend(load_better_json(fqp))
			else:
				if "mismatch" not in fn:
					ret.extend(load_better_json(fqp))

	print("Loaded %s test-cases!" % len(ret))
	return ret


def comment_mismatches_in_file(to_comment_lines, fqp):
	with open(fqp) as fp:
		conts = fp.readlines()


	changed = False

	for idx, line in enumerate(conts):
		# print(idx, line.strip(), any([tmp in line for tmp in to_comment_lines]))
		if any([tmp in line for tmp in to_comment_lines]):
			if not line.strip().startswith("#"):
				changed = True
				# print("Changing '%s'" % (conts[idx], ))
				conts[idx] = "	# " + conts[idx].lstrip()
				# print("To '%s'" % (conts[idx], ))

	if changed:
		print("Should rewrite file!")
		with open(fqp, "w") as fp:
			fp.write("".join(conts))


def comment_mismatches(to_comment_lines, mismatch=False):

	to_comment_lines = [tmp.strip() for tmp in to_comment_lines]

	cdir = os.path.join(os.path.dirname(__file__), "title_data")
	files = os.listdir(cdir)
	for fn in files:
		if ('mismatch' in fn and mismatch == False) or (
			'mismatch' not in fn and mismatch == True):
			print("Skipping commenting in file '%s'" % fn)
		else:
			if fn.endswith(".pyson"):
				fqp = os.path.join(cdir, fn)
				print("Parsing pyson file: ", fn)
				changes = comment_mismatches_in_file(to_comment_lines, fqp)


def test():

	test_data = load_test_data()

	# from tests.title_test_data_two import data as test_data_more
	count = 0
	mismatch = 0
	mismatches = []
	for key, value in tqdm.tqdm(test_data):
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
				# print(p)
				# print("Parsed: v{}, c{}, f{}".format(vol, chp, frag))
				# print("Expect: v{}, c{}, f{}".format(e_vol, e_chp, e_frag))
				# print()

			if e_post != post:
				bad = True
				# print(p)
				# print("Post mismatch - Parsed: {}".format(post))
				# print("Post mismatch - Expect: {}".format(e_post))

			if bad:

				# Row structure is ('Name', (vol, chp, frag, postfix)),
				mismatches.append(
						(
							(key, (e_vol, e_chp, e_frag, e_post)),
							(key, (vol, chp, frag, post)),
						)
					)

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

	with open("title_disconnects.json", "w") as fp:
		json.dump(mismatches, fp, indent=4)

def extract_mismatch():

	# try:

	# 	with open("mismatches.json", "r") as fp:
	# 		remlines = json.load(fp)


	# except (json.JSONDecodeError, FileNotFoundError):


	test_data = load_test_data(mismatch=False)


	count = 0
	mismatch = 0

	test_data_dict = {}


	for item in test_data:
		try:
			key, value = item
		except Exception:
			pprint.pprint(item)
			raise
		test_data_dict.setdefault(key, [])
		test_data_dict[key].append(value)

	remlines = []

	if os.path.exists("tests/title_data/title_test_data_mismatch.pyson"):
		raise RuntimeError("Mismatch file already exists. Not overwriting!")

	existing_entries = []



	with open("tests/title_data/title_test_data_mismatch.pyson", 'w') as fp:
		fp.write("[\n")
		goodstr = []
		badstr = []
		errored = []
		for key, value in tqdm.tqdm(test_data_dict.items()):
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
						# print(p)
						# print("Parsed: v{}, c{}, f{}".format(vol, chp, frag))
						# print("Expect: v{}, c{}, f{}".format(e_vol, e_chp, e_frag))
						# print()

					if e_post != post:
						bad = True
						# print(p)
						# print("Post mismatch - Parsed: {}".format(post))
						# print("Post mismatch - Expect: {}".format(e_post))

					if bad:
						mismatch += 1


					if vol != e_vol or chp != e_chp or frag != e_frag or e_post != post:
						badtmp, remline = format_double_row(key,
									output_volume   = e_vol,
									output_chapter  = e_chp,
									output_fragment = e_frag,
									output_postfix  = e_post,
									expect_volume   = vol,
									expect_chapter  = chp,
									expect_fragment = frag,
									expect_postfix  = post,
								)
						remlines.append(remline)
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

		fp.write("	# Lines with parse mismatches: %s" % (len(badstr), ))
		fp.write("\n\n")
		fp.write("".join(badstr))
		fp.write("\n\n")
		fp.write("	# Errored lines: %s" % (len(errored), ))
		fp.write("\n\n")
		fp.write("".join(errored))
		fp.write("	# Old lines: %s" % (len(existing_entries), ))
		fp.write("\n\n")
		fp.write("".join(existing_entries))

		fp.write("]\n")

	# print("All matches passed!")
	print("{} Items with parsed output".format(count))
	print("{} Items mismatch in new parser".format(mismatch))
	print("{} error encountered in parsing".format(len(errored)))
	print("Total items: {}".format(len(test_data)))

	# with open("mismatches.json", "w") as fp:
	# 	json.dump(remlines, fp, indent=4)

	comment_mismatches(remlines)

def test_mismatch():
	test_data = load_test_data(only_mismatch=True)
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

def format_double_row(title, output_volume, output_chapter, output_fragment, output_postfix,
	                         expect_volume, expect_chapter, expect_fragment, expect_postfix
		):
	real_cont   = str((title, (output_volume, output_chapter, output_fragment, output_postfix)))
	expect_cont = str((title, (expect_volume, expect_chapter, expect_fragment, expect_postfix)))
	return (
			"	# " + expect_cont + ",  # Parsed output\n" +
			"	" + real_cont + ",  # Expected output\n\n"
		), real_cont

def format_row(title, volume, chapter, fragment, postfix):
	cont = str((title, (volume, chapter, fragment, postfix)))
	return "	" + cont + ",\n"


def create_data_file(prefix, outdir, bin_cont):
	print("Bin for {} has {} items".format(prefix, len(bin_cont)))

	bin_cont.sort(key=lambda x: x[0])

	# p_str = ord(prefix) if len(prefix) == 1 and prefix not in string.ascii_lowercase+string.digits else prefix
	pad = ""
	cnt = 0
	while (1):
		mod_name = "'{}'_titles{}.pyson".format(prefix, pad)

		fpath = os.path.join(outdir, mod_name)
		if not os.path.exists(fpath):
			break
		pad = "_({})".format(cnt)
		cnt += 1

	dat = pprint.pformat(bin_cont)

	with open(fpath, "w") as fp:
		fp.write("\n\n")
		fp.write("# Titles for releases starting with the character '{}'".format(prefix))
		fp.write("\n\n")
		fp.write("[\n")
		for item in bin_cont:
			dat = pprint.pformat(item, width=99999999)
			fp.write("	{},\n".format(dat))

		fp.write("]\n\n")

	return mod_name


# def test():
# 	dataset = []
# 	for key, value in test_data:
# 		if len(value) == 2:
# 			e_chp, e_vol = value
# 			dataset.append((key, (e_vol, e_chp, None, None)))
# 		elif len(value) == 4:
# 			e_vol, e_chp, e_frag, e_post = value
# 			dataset.append((key, (e_vol, e_chp, e_frag, e_post)))
# 		else:
# 			print("Wat?", key, value)

# 	print("Loaded {} item dataset".format(len(dataset)))
# 	dataset.sort(key=lambda x: x[0])

# 	bins = {}
# 	for row in dataset:
# 		prefix = row[0].lower()
# 		if prefix:
# 			prefix = prefix[0]
# 		bins.setdefault(prefix, [])
# 		bins[prefix].append(row)

# 	print("Prefix bins: {}".format(len(bins)))
# 	outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'title_data'))
# 	print("Output dir:", outdir)

# 	small_bin = []
# 	for key in list(bins.keys()):
# 		if len(bins[key]) < 10:
# 			dat = bins.pop(key)
# 			small_bin.extend(dat)

# 	bins['other'] = small_bin

# 	print("Prefix bins after consolidation: {}".format(len(bins)))
# 	mod_list = []
# 	for prefix in bins.keys():
# 		mod = create_data_file(prefix, outdir, bins[prefix])
# 		mod_list.append(mod)


# 	load_test_data()


def create_set_files_for_values(new_set):

	bins = {}
	for row in new_set:
		prefix = row[0].lower()
		if prefix:
			prefix = prefix[0]
		bins.setdefault(prefix, [])
		bins[prefix].append(row)

	print("Prefix bins: {}".format(len(bins)))
	outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'title_data'))
	print("Output dir:", outdir)

	small_bin = []
	for key in list(bins.keys()):
		if len(bins[key]) < 10:
			dat = bins.pop(key)
			small_bin.extend(dat)

	bins['other'] = small_bin

	print("Prefix bins after consolidation: {}".format(len(bins)))
	mod_list = []
	for prefix in bins.keys():
		mod = create_data_file(prefix, outdir, bins[prefix])
		mod_list.append(mod)


def merge_in_fixed_mismatch():

	test_data = load_test_data(only_mismatch=True)
	count = 0
	mismatch = 0


	remlines = []
	good_lines = []
	good_sets = []

	for key, value in test_data:

		p = TPN(key)
		vol, chp, frag, post = p.getVolume(), p.getChapter(), p.getFragment(), p.getPostfix()

		e_vol, e_chp, e_frag, e_post = value

		if vol != e_vol or chp != e_chp or frag != e_frag or e_post != post:
			badtmp, remline = format_double_row(key,
						output_volume   = e_vol,
						output_chapter  = e_chp,
						output_fragment = e_frag,
						output_postfix  = e_post,
						expect_volume   = vol,
						expect_chapter  = chp,
						expect_fragment = frag,
						expect_postfix  = post,
					)
			remlines.append(remline)
		else:
			goodtmp = format_row(key, e_vol, e_chp, e_frag, e_post)
			good_lines.append(goodtmp)
			good_sets.append((key, value))

		count += 1


	# print("All matches passed!")
	print("{} Items with parsed output".format(count))
	print("{} Items mismatch in new parser".format(len(remlines)))
	print("{} OK lines".format(len(good_lines)))
	print("Total items: {}".format(len(test_data)))
	if good_lines:
		comment_mismatches(good_lines, mismatch=True)
		create_set_files_for_values(good_sets)

# def load_items():
# 	feed_items = db.get_db_session().query(db.RssFeedPost) \
# 			.order_by(db.RssFeedPost.srcname)           \
# 			.order_by(db.RssFeedPost.title)           \
# 			.all()

# 	with open("tests/title_test_data_two.py", 'w') as fp:
# 		fp.write("data = [\n")
# 		for row in feed_items:
# 			title = row.title

# 			try:
# 				p = TPO(title)
# 				fp.write(format_row(title, p.getVolume(), p.getChapter(), p.getFragment(), p.getPostfix()))
# 			except ValueError:
# 				fp.write(format_row(title, 0, 0, 0, ''))

# 		fp.write("]\n")

if __name__ == "__main__":
	import sys
	# if 'regenerate' in sys.argv:
	# 	load_items()
	if "extract-mismatch" in sys.argv:
		extract_mismatch()
	elif "test-mismatch" in sys.argv:
		test_mismatch()
	elif "merge-in-mismatch" in sys.argv:
		merge_in_fixed_mismatch()
	elif "load" in sys.argv:
		load_test_data()
	else:
		print("No command")
		# test()

