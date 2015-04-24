from flask import Flask, jsonify, request, g
from models import *
from crossdomain import crossdomain

app = Flask(__name__)

data = {
    'name' : 'Iyengar Weeks 3 and 4',
    'duration' : 10,
    'poses' : [
        {
            'id': 0,
            'name': 'Utthita Trikonasana',
            'easy_name': 'Triangle',
            'time': 5,
        },
        {
            'id': 1,
            'name': 'Utthita Parsvakonasana',
            'easy_name': 'Extended Side Angle',
            'time': 5,
        },
    ],
}

@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db_session = create_session()

@app.route('/api/sequence')
@crossdomain(origin='*')
def index():
    return jsonify(data)

@app.route('/api/pose', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers='accept, content-type')
def add_pose():

    print request.json
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

if __name__ == '__main__':
    app.run(debug=True)
