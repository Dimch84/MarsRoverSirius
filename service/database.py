from sqlalchemy.orm import declarative_base
from sqlalchemy import *

Base = declarative_base()


class Service(Base):
    __tablename__ = 'team_service'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    url = Column(String)

    def __repr__(self):
        return f'Service(id={self.id!r}, name={self.name!r}, url={self.url!r})'


engine = create_engine("sqlite+pysqlite:///db/", echo=True)
Base.metadata.create_all(engine)
