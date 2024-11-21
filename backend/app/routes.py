from flask import Blueprint, jsonify

bp = Blueprint('routes', __name__)


@bp.route('/api/data', methods=['GET'])
def get_data():
    # Dummy Daten
    data = [
        {"time": "2023-01-01", "value": 10},
        {"time": "2023-01-02", "value": 40},
        {"time": "2023-01-03", "value": 20},
        {"time": "2023-01-04", "value": 30},
        {"time": "2023-01-05", "value": 60},
    ]

    return jsonify(data)
