
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


out_a_g = open('ParserFuncs_a_g.py', "a")
out_h_n = open('ParserFuncs_h_n.py', "a")
out_o_u = open('ParserFuncs_o_u.py', "a")
out_v_other = open('ParserFuncs_v_other.py', "a")



for key, value in vals.items():
	key = key[len("extract"):]
	letter = key[0].lower()
	if letter in "abcdefg":
		out_a_g.write("\n")
		out_a_g.write(value)
		out_a_g.write("\n")

	elif letter in "hijklmn":
		out_h_n.write("\n")
		out_h_n.write(value)
		out_h_n.write("\n")

	elif letter in "opqrstu":
		out_o_u.write("\n")
		out_o_u.write(value)
		out_o_u.write("\n")

	else:
		out_v_other.write("\n")
		out_v_other.write(value)
		out_v_other.write("\n")

