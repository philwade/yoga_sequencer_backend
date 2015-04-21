from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

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
    sequencePoses = relationship('SequencePose', backref=backref('pose'))

class Sequence(Base):
    __tablename__ = 'sequence'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    sequencePoses = relationship('SequencePose', backref=backref('sequence'))

class SequencePose(Base):
    __tablename__ = 'sequence_pose'

    id = Column(Integer, primary_key=True)
    sequence_id = Column(Integer, ForeignKey('sequence.id'))
    pose_id = Column(Integer, ForeignKey('pose.id'))
    duration = Column(Integer)
    ordinality = Column(Integer)

    sequence = relationship('Sequence', backref=backref('sequencePoses'))
    pose = relationship('Pose', backref=backref('sequencePoses'))
