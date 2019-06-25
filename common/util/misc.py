
import tqdm

def batch(iterable, n=1, show_progress=False):
	l = len(iterable)

	show_progress = False

	if show_progress:
		for ndx in tqdm.tqdm(range(0, l, n)):
			yield iterable[ndx:min(ndx + n, l)]
	else:
		for ndx in range(0, l, n):
			yield iterable[ndx:min(ndx + n, l)]
