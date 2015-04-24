from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker

DEBUG=True
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

class Pose(Base):
    __tablename__ = 'pose'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    simplename = Column(String)

    def json(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Sequence(Base):
    __tablename__ = 'sequence'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class SequencePose(Base):
    __tablename__ = 'sequence_pose'

    id = Column(Integer, primary_key=True)
    sequence_id = Column(Integer, ForeignKey('sequence.id'))
    pose_id = Column(Integer, ForeignKey('pose.id'))
    duration = Column(Integer)
    ordinality = Column(Integer)

    sequence = relationship('Sequence', backref=backref('sequencePoses'))
    pose = relationship('Pose', backref=backref('sequencePoses'))

def create_session():
    engine = create_engine("sqlite:///test.db")
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

if __name__ == '__main__':
    engine = create_engine("sqlite:///test.db")
    Base.metadata.create_all(engine)
    session = create_session()

    triangle = Pose(
        name='Utthita Trikonasana',
        simplename='Triangle',
    )

    side = Pose(
            name='Utthita Parsvakonasana',
            simplename='Extended Side Angle',
    )

    session.add(triangle)
    session.add(side)
    session.commit()
