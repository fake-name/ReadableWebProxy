
with open('ParserFuncs.py') as fp:
	content = fp.read()

cspl = content.split("\ndef")

vals = {}
for item in cspl:
	if item.strip() == "":
		continue
	fname = item.split("(")[0].strip()
	if fname in vals:
		raise ValueError("Wat? %s" % fname)
	vals[fname] = "def " + item


out_a_g = open('ParserFuncs_a_g.py')
out_h_n = open('ParserFuncs_h_n.py')
out_o_u = open('ParserFuncs_o_u.py')
out_v_other = open('ParserFuncs_v_other.py')



for key, value in vals.items():
	key = key[len("extract"):]
	letter = key[0].lower()
	if letter in "abcdefg":
		print(key)

