#!/usr/bin/env bash

# Halt on errors.
set -e

# This is just a very minimal script that starts the scraper.
echo "Updating local git repo"
git fetch --all
git pull


echo "Available branches:"
git --no-pager branch -a | cat


echo "Current release:"
git --no-pager log -1 | cat

if [ -d "venv" ]
then
	echo "Venv exists. Activating!"
	source venv/bin/activate
else
	echo "No Venv! Checking dependencies are installed."
	sudo apt-get update
	sudo apt-get install build-essential -y
	sudo apt-get install libfontconfig -y
	sudo apt-get install libxml2 libxslt1-dev python3-dev libz-dev -y

	# 16.04 phantomjs apt package is fucked, crashes on start.
	# sudo apt-get install phantomjs -y
	wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
	tar -xvf phantomjs-2.1.1-linux-x86_64.tar.bz2
	mv ./phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/
	rm -rf phantomjs-2.1.1-linux-x86_64
	echo "Creating venv."

	python3 -m venv --without-pip venv
	wget https://bootstrap.pypa.io/get-pip.py
	./venv/bin/python3 get-pip.py
	rm get-pip.py
	source venv/bin/activate
	./venv/bin/pip install cython
	./venv/bin/pip install requests

fi;

./venv/bin/pip install --upgrade -r requirements.txt

# If we're in a docker instance, the credentials will have been passed in as a
# env var. Therefore, dump them to the settings.json file.
if [ -z "$SCRAPE_CREDS" ];
then
	echo "SCRAPE_CREDS is unset!"
else
	echo "SCRAPE_CREDS is set!"
fi;

echo "Launching executable."
python3 ./run.py
