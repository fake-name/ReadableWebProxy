#!/bin/bash

# So ubuntu continues to spectacularly fuck up their python distro, in this
# case the broke parts of pip (which is now baked into python 3 by default).
# see https://bugs.launchpad.net/ubuntu/+source/python3/+bug/1290847

# Anyways, build a venv that works.

python3 -m venv --without-pip venv
wget https://bootstrap.pypa.io/get-pip.py
./venv/bin/python3 get-pip.py
rm get-pip.py
./venv/bin/pip install --upgrade -r requirements.txt