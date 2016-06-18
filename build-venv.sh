#!/bin/bash

# So ubuntu continues to spectacularly fuck up their python distro, in this
# case the broke parts of pip (which is now baked into python 3.4 by default).
# see https://bugs.launchpad.net/ubuntu/+source/python3.4/+bug/1290847

# Anyways, build a venv that works.

sudo apt-get update
sudo apt-get install build-essential -y
sudo apt-get install libfontconfig -y
sudo apt-get install libxml2 libxml2-dev libxslt1-dev libxslt-devel python3-dev libz-dev zlib1g-dev -y
sudo apt-get install libxml2-dev libxslt-dev -y

python3.5 -m venv --without-pip flask
wget https://bootstrap.pypa.io/get-pip.py
./flask/bin/python get-pip.py
rm get-pip.py


./flask/bin/pip install --upgrade -r requirements.txt