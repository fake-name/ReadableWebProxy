import os.path
import string
import pprint

# from FeedScrape.FeedDataParser import extractChapterVol
from tests.title_test_data import data as test_data
from WebMirror.OutputFilters.util.TitleParsers import TitleParser

def create_data_file(prefix, outdir, bin_cont):
	print("Bin for {} has {} items".format(prefix, len(bin_cont)))

	bin_cont.sort()

	p_str = ord(prefix) if len(prefix) == 1 and prefix not in string.ascii_lowercase+string.digits else prefix
	mod_name = "data_{}_set".format(p_str)
	fpath = os.path.join(outdir, "{}.py".format(mod_name))
	dat = pprint.pformat(bin_cont)

	with open(fpath, "w") as fp:
		fp.write("\n\n")
		fp.write("data = [\n")
		for item in bin_cont:
			dat = pprint.pformat(item, width=99999999)
			fp.write("	{},\n".format(dat))

		fp.write("]\n\n")

	return mod_name

def create__init__file(outdir, mod_list):
	fpath = os.path.join(outdir, "__init__.py")

	mod_list.sort()

	with open(fpath, "w") as fp:
		fp.write("\n\n")
		for mod in mod_list:
			fp.write("from .{} import data as {}_data\n".format(mod, mod))
		fp.write("\n\n")

		fp.write("data_map = {\n")
		for mod in mod_list:
			fp.write("	'{}' : {}_data,\n".format(mod, mod))
		fp.write("}\n\n")

def test_load():
	print("attempting to import generated source")
	from .title_data import data_map
	print("Loaded source OK")
	print("Found %s keys" % len(data_map))
	print("Total data items: %s" % sum([len(tmp) for tmp in data_map.values()]))


def test():
	dataset = []
	for key, value in test_data:
		if len(value) == 2:
			e_chp, e_vol = value
			dataset.append((key, e_vol, e_chp, None, None))
		elif len(value) == 4:
			e_vol, e_chp, e_frag, e_post = value
			dataset.append((key, e_vol, e_chp, e_frag, e_post))
		else:
			print("Wat?", key, value)

	print("Loaded {} item dataset".format(len(dataset)))
	dataset.sort()

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

	create__init__file(outdir, mod_list)

	test_load()

if __name__ == "__main__":

	test()

