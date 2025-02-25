from flask import Blueprint, request, jsonify, redirect
from app.spotify import get_token_from_code, process_spotify_data, get_auth_url

bp = Blueprint('api', __name__)

@bp.route('/auth-url')
def auth_url():
    return jsonify({"auth_url": get_auth_url()})

@bp.route('/callback')
def callback():
    code = request.args.get("code")
    token = get_token_from_code(code)
    if token:
        # Redirect to the frontend with the token as a query parameter.
        return redirect(f"http://localhost:5173?token={token}")
    else:
        return jsonify({"error": "Failed to obtain access token"}), 400

@bp.route('/process-songs', methods=['POST'])
def process_songs():
    data = request.get_json()
    token = data.get("token")
    num_songs = data.get("num_songs", 20)
    target_color = data.get("target_color")  # Extract target color from the request
    if not token:
        return jsonify({"error": "Missing token"}), 400

    result = process_spotify_data(token, num_songs, target_color)
    return jsonify(result)


@bp.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    return response
