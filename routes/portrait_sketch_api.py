"""The Endpoints to manage the BOOK_REQUESTS"""
from flask import request, Blueprint

from io import BytesIO
from urllib.parse import unquote_plus
from urllib.request import urlopen
from flask import send_file
from services.portrait_sketch.portrait_sketch import transform

REQUEST_API = Blueprint('portrait_sketch_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/api/portrait_sketch', methods=['GET', 'POST'])
def portrait_sketch_handler():
    file_content = ""

    if request.method == "POST":
        if "file" not in request.files:
            return {"error": "missing post form param 'file'"}, 400

        file_content = request.files["file"].read()

    if request.method == "GET":
        url = request.args.get("url", type=str)
        if url is None:
            return {"error": "missing query param 'url'"}, 400

        file_content = urlopen(unquote_plus(url)).read()

    if file_content == "":
        return {"error": "File content is empty"}, 400
    try:
        return send_file(
            BytesIO(
                transform( file_content)
            ),
            mimetype="image/png",
        )
    except Exception as e:
        return {"error": "oops, something went wrong!"}, 500

