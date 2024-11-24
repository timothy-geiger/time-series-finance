from flask import jsonify, Blueprint
from influxdb_client import InfluxDBClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(override=True)

bp = Blueprint('api', __name__)

# Load configuration from environment variables
INFLUXDB_URL = os.getenv("INFLUXDB_V2_URL")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_V2_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")


@bp.route('/api/data', methods=['GET'])
def get_data():
    try:
        # Connect to InfluxDB
        client = InfluxDBClient(
            url=INFLUXDB_URL,
            token=INFLUXDB_TOKEN,
            org=INFLUXDB_ORG,
            debug=False)
        query_api = client.query_api()

        # Define InfluxDB Query
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
            |> range(start: -30d)
            |> filter(fn: (r) => r["_measurement"] == "coindesk")
            |> filter(fn: (r) => r["_field"] == "price")
            |> filter(fn: (r) => r["code"] == "EUR")
            |> filter(fn: (r) => r["crypto"] == "bitcoin")
            |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)
            |> yield(name: "mean")
        '''

        # Execute Query
        tables = query_api.query(query=query, org=INFLUXDB_ORG)
        data = []

        for table in tables:
            for record in table.records:
                data.append({
                    "time": record.get_time(),
                    "value": record.get_value()
                })

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
