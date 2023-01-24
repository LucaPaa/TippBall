from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# initialize sqlite connection url
SQLALCHEMY_DATABASE_URL = "sqlite:///./instance/bundesliga.db"
# echo logs the sql statements to console; set to false in production
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)


# create a session to be used by other packages
SessionLocal = sessionmaker(engine)
Base = declarative_base()
