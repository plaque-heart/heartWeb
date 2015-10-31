import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

SQLBase = automap_base()

engine = sqlalchemy.create_engine("sqlite:///dbase.db", echo=True)
session=sessionmaker(bind=engine)()

SQLBase.prepare(engine, reflect=True)

