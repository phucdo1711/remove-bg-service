

"""The Endpoints to manage the BOOK_REQUESTS"""
from flask import request, Blueprint

from io import BytesIO
from urllib.parse import unquote_plus
from urllib.request import urlopen
from flask import send_file
from services.cartoonize.cartoonize import cartoonize
from flask.json import jsonify

REQUEST_API = Blueprint('cartoonize_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/api/cartoonize', methods=['GET', 'POST'])
def cartoonize_handler():
    file_content = ""

    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"error": "missing post form param 'file'"}), 400

        file_content = request.files["file"].read()

    if request.method == "GET":
        url = request.args.get("url", type=str)
        if url is None:
            return jsonify({"error": "missing query param 'url'"}), 400

        file_content = urlopen(unquote_plus(url)).read()

    if file_content == "":
        return jsonify({"error": "File content is empty"}), 400
    try:
        return send_file(
            BytesIO(
                cartoonize(file_content)
            ),
            mimetype="image/png",
        )
    except Exception as e:
        return jsonify({"error": "oops, something went wrong!" + str(e)}), 500


