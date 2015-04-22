from flask import Flask, jsonify
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

@app.route('/api/sequence')
@crossdomain(origin='*')
def index():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
