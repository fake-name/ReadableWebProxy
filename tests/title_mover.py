import os.path
import string
import pprint
import ast

# from FeedScrape.FeedDataParser import extractChapterVol
from tests.title_test_data import data as test_data
from WebMirror.OutputFilters.util.TitleParsers import TitleParser


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

def create_data_file(prefix, outdir, bin_cont):
	print("Bin for {} has {} items".format(prefix, len(bin_cont)))

	bin_cont.sort(key=lambda x: x[0])

	# p_str = ord(prefix) if len(prefix) == 1 and prefix not in string.ascii_lowercase+string.digits else prefix
	mod_name = "'{}'_titles.pyson".format(prefix)
	fpath = os.path.join(outdir, mod_name)
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

def test():
	dataset = []
	for key, value in test_data:
		if len(value) == 2:
			e_chp, e_vol = value
			dataset.append((key, (e_vol, e_chp, None, None)))
		elif len(value) == 4:
			e_vol, e_chp, e_frag, e_post = value
			dataset.append((key, (e_vol, e_chp, e_frag, e_post)))
		else:
			print("Wat?", key, value)

	print("Loaded {} item dataset".format(len(dataset)))
	dataset.sort(key=lambda x: x[0])

	bins = {}
	for row in dataset:
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


	load_test_data()

if __name__ == "__main__":

	test()

