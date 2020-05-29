
import psutil


def is_low_mem():
	v = psutil.virtual_memory()

	threshold = v.total / 4

	# If we have less then 25% ram free, we should stop feeding the job system.
	if v.available < threshold:
		return True
	return False

