from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key = True)

    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)
    
    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)

Base.metadata.create_all(bind=engine)

s = session()
news = News(title='Lab 7', 
                author='dementiy',
                url='https://dementiy.gitbooks.io/-python/content/lab7.html',
                comments=0,
                points=0)

s.add(news)
s.commit()