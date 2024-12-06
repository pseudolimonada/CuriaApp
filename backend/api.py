from flask import Flask, request, jsonify
from flask_cors import CORS
from db_models import VisualizationData
import json
from config import Config
from extensions import db

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

app.config.from_object(Config)
db.init_app(app)  # Initialize the db instance with the app
print("Frontend at http://127.0.0.1:8000/")
print("Backend at http://127.0.0.1:5000/")


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Hello, World!"}), 200


@app.route("/get_all_data", methods=["GET"])
def add_repo():
    repo_url = request.args.get("repo_url")
    auth_header = request.headers.get("Authorization")

    if not repo_url:
        return jsonify({"error": "Missing repo_url"}), 400

    if not auth_header:
        return jsonify({"error": "Missing Authorization header"}), 400

    # Extract the token from the Authorization header
    token = None
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]

    if not token:
        return jsonify({"error": "Invalid Authorization header"}), 400

    result, code = gitlab_get_all_data(repo_url, token)

    return jsonify(result), code


@app.route("/list_repositories", methods=["GET"])
def list_repositories():
    data = VisualizationData.query.all()
    repos = set()
    for d in data:
        repos.add(d.repo_id)
    return jsonify(list(repos)), 200


@app.route("/visualization1", methods=["GET"], strict_slashes=False)
def visualization1():
    repo_url = request.args.get("repo_url")
    if not repo_url:
        return jsonify({"error": "Missing repo_url"}), 400
    data = VisualizationData.query.filter_by(
        repo_id=repo_url, visualization_type="visualization1"
    ).first()
    if not data:
        return jsonify({"error": "Data not found"}), 404
    json_data = json.loads(data.json_data)
    # Process json_data based on optional filters
    processed_data = process_visualization1(json_data, request.args)
    return jsonify(processed_data), 200


@app.route("/histogram_loc", methods=["GET"])
def histogram_loc():
    repo_url = request.args.get("repo_url")
    if not repo_url:
        return jsonify({"error": "Missing repo_url"}), 400
    data = VisualizationData.query.filter_by(
        repo_id=repo_url, visualization_type="histogram_loc"
    ).first()
    if not data:
        return jsonify({"error": "Data not found"}), 404
    json_data = json.loads(data.json_data)
    # Process json_data based on optional filters
    processed_data = process_histogram_loc(json_data, request.args)
    return jsonify(processed_data), 200


@app.route("/histogram_authors", methods=["GET"])
def histogram_authors():
    repo_url = request.args.get("repo_url")
    if not repo_url:
        return jsonify({"error": "Missing repo_url"}), 400

    # Retrieve data from the database
    data = VisualizationData.query.filter_by(
        repo_id=repo_url, visualization_type="histogram_authors"
    ).first()
    if not data:
        return jsonify({"error": "Data not found"}), 404
    json_data = json.loads(data.json_data)  # Load JSON data

    # Process data based on optional filters
    processed_data = process_author_ranges(json_data, request.args)

    # Return the processed data
    return jsonify(processed_data), 200


@app.route("/histogram_cyc_complexity", methods=["GET"])
def histogram_cyc_complexity():
    repo_url = request.args.get("repo_url")
    if not repo_url:
        return jsonify({"error": "Missing repo_url"}), 400

    data = VisualizationData.query.filter_by(
        repo_id=repo_url, visualization_type="histogram_cyc_complexity"
    ).first()
    if not data:
        return jsonify({"error": "Data not found"}), 404

    json_data = json.loads(data.json_data)

    # Process data based on optional filters
    processed_data = process_cyclomatic_complexity_ranges(json_data, request.args)

    # Return the processed data
    return jsonify(processed_data), 200


@app.route("/histogram_commits_per_file", methods=["GET"])
def histogram_commits():
    repo_url = request.args.get("repo_url")
    if not repo_url:
        return jsonify({"error": "Missing repo_url"}), 400
    # Retrieve data from the database
    data = VisualizationData.query.filter_by(
        repo_id=repo_url, visualization_type="histogram_commits_per_file"
    ).first()
    if not data:
        return jsonify({"error": "Data not found"}), 404

    # Load JSON data
    json_data = json.loads(data.json_data)

    # Process data based on optional filters
    processed_data = process_commit_ranges(json_data, request.args)

    # Return the processed data
    return jsonify(processed_data), 200


def process_visualization1(json_data, filters):
    # Implement the processing logic based on filters
    return json_data


def process_histogram_loc(json_data, filters):
    # Retrieve optional filters
    interval_size = int(filters.get("interval_size", 10))  # Default interval size is 10
    min_val = int(filters.get("min", min(json_data.values())))
    max_val = int(filters.get("max", max(json_data.values())))

    # Validate inputs
    if interval_size <= 0 or min_val >= max_val:
        return {"error": "Invalid interval size or range"}, 400

    # Initialize the interval counts
    intervals = {}
    for start in range(min_val, max_val + 1, interval_size):
        end = start + interval_size - 1
        intervals[f"{start}-{end}"] = 0

    # Count files in each interval
    for loc in json_data.values():
        for start in range(min_val, max_val + 1, interval_size):
            end = start + interval_size - 1
            if start <= loc <= end:
                intervals[f"{start}-{end}"] += 1
                break

    return intervals  # return json_data in the form of: {"0-5": 5, "6-10": 10, ...}


def process_author_ranges(json_data, filters):
    # Retrieve optional filters
    interval_size = int(filters.get("interval_size", 5))  # Default interval size is 5
    min_val = int(filters.get("min", min(json_data.values())))
    max_val = int(filters.get("max", max(json_data.values())))

    # Validate inputs
    if interval_size <= 0 or min_val >= max_val:
        return {"error": "Invalid interval size or range"}, 400

    # Initialize the interval counts
    intervals = {}
    for start in range(min_val, max_val + 1, interval_size):
        end = start + interval_size - 1
        intervals[f"{start}-{end}"] = 0

    # Count files in each interval
    for author_count in json_data.values():
        for start in range(min_val, max_val + 1, interval_size):
            end = start + interval_size - 1
            if start <= author_count <= end:
                intervals[f"{start}-{end}"] += 1
                break

    return intervals


def process_cyclomatic_complexity_ranges(json_data, filters):
    # Retrieve optional filters
    interval_size = int(filters.get("interval_size", 10))  # Default interval size is 10
    min_val = int(filters.get("min", min(json_data.values())))
    max_val = int(filters.get("max", max(json_data.values())))

    # Validate inputs
    if interval_size <= 0 or min_val >= max_val:
        return {"error": "Invalid interval size or range"}, 400

    # Initialize the interval counts
    intervals = {}
    for start in range(min_val, max_val + 1, interval_size):
        end = start + interval_size - 1
        intervals[f"{start}-{end}"] = 0

    # Count files in each interval
    for complexity in json_data.values():
        for start in range(min_val, max_val + 1, interval_size):
            end = start + interval_size - 1
            if start <= complexity <= end:
                intervals[f"{start}-{end}"] += 1
                break

    return intervals


def process_commit_ranges(json_data, filters):
    # Retrieve optional filters
    interval_size = int(filters.get("interval_size", 10))  # Default interval size is 10
    min_val = int(filters.get("min", min(json_data.values())))
    max_val = int(filters.get("max", max(json_data.values())))

    # Validate inputs
    if interval_size <= 0 or min_val >= max_val:
        return {"error": "Invalid interval size or range"}, 400

    # Initialize the interval counts
    intervals = {}
    for start in range(min_val, max_val + 1, interval_size):
        end = start + interval_size - 1
        intervals[f"{start}-{end}"] = 0

    # Count files in each interval
    for commit_count in json_data.values():
        for start in range(min_val, max_val + 1, interval_size):
            end = start + interval_size - 1
            if start <= commit_count <= end:
                intervals[f"{start}-{end}"] += 1
                break

    return intervals


if __name__ == "__main__":
    app.run(debug=True)
