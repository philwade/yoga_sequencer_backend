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

    def json(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Pose(Base):
    __tablename__ = 'pose'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    simplename = Column(String)

    def json(self):

        json_rep = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        # this will need to be a wiser selector when we have multiple images
        if self.PoseImages:
            json_rep['poseImage'] = self.PoseImages[0].json()

        return json_rep

class PoseImage(Base):
    __tablename__ = 'pose_image'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    author = Column(String)
    license = Column(String)
    further_attribution = Column(String)
    pose_id = Column(Integer, ForeignKey('pose.id'))

    pose = relationship('Pose', backref=backref('PoseImages'))

    def json(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Sequence(Base):
    __tablename__ = 'sequence'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    default_duration = Column(Integer)

    def json(self):
       json_rep = {c.name: getattr(self, c.name) for c in self.__table__.columns}

       json_rep['sequencePoses'] = [pose.json() for pose in self.sequencePoses]

       return json_rep

class SequencePose(Base):
    __tablename__ = 'sequence_pose'

    id = Column(Integer, primary_key=True)
    sequence_id = Column(Integer, ForeignKey('sequence.id'))
    pose_id = Column(Integer, ForeignKey('pose.id'))
    duration = Column(Integer)
    ordinality = Column(Integer)

    sequence = relationship('Sequence', backref=backref('sequencePoses', order_by=ordinality))
    pose = relationship('Pose', backref=backref('sequencePoses'))

    def json(self):
       json_rep = {c.name: getattr(self, c.name) for c in self.__table__.columns}

       json_rep['pose'] = self.pose.json()

       return json_rep

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

    session.commit()
