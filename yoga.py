from flask import Flask, jsonify, request, g
from models import *
from crossdomain import crossdomain

app = Flask(__name__)

@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db_session = create_session()

@app.route('/api/sequence')
@crossdomain(origin='*')
def index():
    sequence = g.db_session.query(Sequence).first()
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

@app.route('/api/pose/search', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers='accept, content-type')
def search():
    searchTerm = request.json['search']
    poses = g.db_session.query(Pose).filter(Pose.name.like('%' + searchTerm + '%')).all()

    return jsonify({'results':[pose.json() for pose in poses]})

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
