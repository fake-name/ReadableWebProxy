# From https://gist.github.com/destan/5540702#file-text2png-py

# coding=utf8

import multiprocessing
import threading
import time
import atexit
import os

import vmprof

def install_vmprof(name="thread"):

	cpid = multiprocessing.current_process().name
	ctid = threading.current_thread().name
	fname = "vmprof-{}-{}-{}-{}.dat".format(name, cpid, ctid, time.time())


	flags = os.O_RDWR | os.O_CREAT | os.O_TRUNC
	outfd = os.open(fname, flags)
	vmprof.enable(outfd, period=0.01)

	atexit.register(close_profile_file)

def close_profile_file():

	vmprof.disable()
