
import functools
import datetime
import xxhash

starttime = datetime.datetime(2020, 1, 1)

def hash_netloc(netloc):

	m = xxhash.xxh32()
	m.update(netloc.encode("utf-8"))
	nlhash = m.intdigest()

	return nlhash

def get_epoch_from_netloc_interval(netloc, interval_days):
	'''
	from a netloc and a rewalk interval, return the current epoch
	for that netloc.

	The epoch should increment by 1 every interval_days, with the point in interval_days
	at which it increments being evenly distrubuted across the interval assuming
	a fairly large number of netlocs.
	'''

	nlhash = hash_netloc(netloc)
	rewalk_offset = nlhash % interval_days
	# print("Rewalk offset", rewalk_offset)
	delta = datetime.datetime.now() - starttime
	offset = delta.days + rewalk_offset

	return int(offset // interval_days)

def test():
	res = {}
	for x in range(50000):
		ret = get_epoch_from_netloc_interval("test" + "t" * x, 60)
		res.setdefault(ret, 0)
		res[ret] += 1
	print(res)

	res = {}
	for x in range(50000):
		ret = get_epoch_from_netloc_interval("test" + "t" * x, 30)
		res.setdefault(ret, 0)
		res[ret] += 1
	print(res)

	res = {}
	for x in range(50000):
		ret = get_epoch_from_netloc_interval("test" + "t" * x, 45)
		res.setdefault(ret, 0)
		res[ret] += 1

	print(res)
	# print(get_epoch_from_netloc_interval("testt", 60))
	# print(get_epoch_from_netloc_interval("testtt", 60))
	# print(get_epoch_from_netloc_interval("testttt", 60))
	# print(get_epoch_from_netloc_interval("testtttt", 60))


if __name__ == '__main__':
	import cProfile
	cProfile.run('test()', sort="cumulative")
	# test()
