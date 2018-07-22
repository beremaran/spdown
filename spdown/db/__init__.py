#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from spdown.db.models import *
from spdown.config import Config

config = Config()
db_path = config.get('database_path')
del config
del Config

engine = create_engine('sqlite:///{}'.format(db_path), echo=False)
Base.metadata.create_all(engine)
session = sessionmaker()
session.configure(bind=engine)
session = session()
