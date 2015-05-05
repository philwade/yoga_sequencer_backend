from flask import Flask, jsonify, request, g
from models import *
from sqlalchemy import or_
from crossdomain import crossdomain

app = Flask(__name__)

@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db_session = create_session()

@app.route('/api/sequence/list', methods=['GET'])
@crossdomain(origin='*')
def sequence_list():
    sequences = g.db_session.query(Sequence).all()
    return jsonify({'sequences': [sequence.json() for sequence in sequences]})

@app.route('/api/sequence/<int:sequence_id>', methods=['GET'])
@app.route('/api/sequence')
@crossdomain(origin='*')
def index(sequence_id=None):
    if sequence_id == None:
        sequence = Sequence()
    else:
        sequence = g.db_session.query(Sequence).filter_by(id=sequence_id).one()
    return jsonify(sequence.json())

@app.route('/api/pose', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers='accept, content-type')
def add_pose():

    try:
        id = request.json['id']
    except AttributeError:
        id = None

    pose = Pose(
        id = id,
        name = request.json['name'],
        simplename = request.json['simplename'],
    )

    g.db_session.merge(pose)
    g.db_session.commit()

    return jsonify(pose.json())

@app.route('/api/pose/<int:pose_id>', methods=['GET'])
@app.route('/api/pose', methods=['GET'])
@crossdomain(origin='*')
def get_pose(pose_id=None):
    if pose_id == None:
        pose = Pose()
    else:
        pose = g.db_session.query(Pose).filter_by(id=pose_id).one()
    return jsonify(pose.json())

@app.route('/api/sequencepose/<int:pose_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_sequencepose(pose_id):
    pose = g.db_session.query(SequencePose).filter_by(id=pose_id).one()
    g.db_session.delete(pose)
    return


@app.route('/api/pose/search', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers='accept, content-type')
def search():
    searchTerm = request.json['search']
    poses = g.db_session.query(Pose).filter(or_(Pose.name.like('%' + searchTerm + '%'), Pose.simplename.like('%' + searchTerm + '%'))).all()

    return jsonify({'results':[pose.json() for pose in poses]})

@app.route('/api/sequence/save', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers='accept, content-type')
def save_sequence():
    jsonsequence = request.json['sequence']
    todelete = request.json['toRemove']

    sequencePoses = g.db_session.query(SequencePose).filter(SequencePose.id.in_(todelete)).all()
    for sequencePose in sequencePoses:
        g.db_session.delete(sequencePose)

    sequence = Sequence(
        id = jsonsequence['id'],
        name = jsonsequence['name'],
        description = jsonsequence['description'],
        default_duration = jsonsequence['default_duration'],
    )
    sequencePoses = [_sequencePose_from_json(sq, sequence) for sq in jsonsequence['sequencePoses']]
    sequence.sequencePoses = sequencePoses

    g.db_session.merge(sequence)
    g.db_session.commit()

    return jsonify(sequence.json())

def _sequencePose_from_json(jsonsq, sequence):
    try:
        id = jsonsq['id']
    except KeyError:
        id = None

    sequencePose = SequencePose(
        id = id,
        duration = jsonsq['duration'],
        ordinality = jsonsq['ordinality'],
        pose = _pose_from_json(jsonsq['pose']),
        sequence = sequence,
    )

    return sequencePose

def _pose_from_json(jsonpose):
    return Pose(
        id = jsonpose['id'],
        name = jsonpose['name'],
        simplename = jsonpose['simplename'],
        PoseImages = [_poseimage_from_json(jsonpose['poseImage'])]
    )

def _poseimage_from_json(jsonposeimage):
    return PoseImage(
        id = jsonposeimage['id'],
        url = jsonposeimage['url'],
        author = jsonposeimage['author'],
        further_attribution = jsonposeimage['further_attribution'],
    )


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
