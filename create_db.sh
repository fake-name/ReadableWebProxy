#! /bin/bash

# Initialize/Reinitialize the database for the app.

# Note: You need pg_trgm and citext extensions installed for this to work.
# On ubuntu: sudo apt-get install postgresql-contrib
# then CREATE EXTENSION citext; CREATE EXTENSION pg_trgm;

set -e

rm -rf ./migrations
python db_migrate.py db init
cp ./script.py.mako ./migrations/
python db_migrate.py db migrate
python db_migrate.py db upgrade

