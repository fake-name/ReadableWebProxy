#!flask/bin/python

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

from app import app, db
from citext import CIText
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import models

Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)



if __name__ == '__main__':
	print("Running migrator!")
	manager.run()

