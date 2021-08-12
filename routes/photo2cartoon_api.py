import os
from flask import request, Blueprint

from io import BytesIO
from urllib.parse import unquote_plus
from urllib.request import urlopen
from flask import send_file
import subprocess
import tempfile

from flask.json import jsonify

REQUEST_API = Blueprint('photo2cartoon_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/api/photo2cartoon', methods=['GET', 'POST'])
def photo2cartoon_handler():
    file = None

    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"error": "missing post form param 'file'"}), 400

        file = request.files["file"]
    elif request.method == "GET":
        url = request.args.get("url", type=str)
        if url is None:
            return jsonify({"error": "missing query param 'url'"}), 400

        file = urlopen(unquote_plus(url))

    if file == None:
        return jsonify({"error": "File content is empty"}), 400

    filename, file_extension = os.path.splitext(file.filename)
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_path = os.path.join(tmpdirname, 'image_input' + file_extension)
        file_result_path = os.path.join(tmpdirname, 'image_result.png')
        file.save(file_path)

        try: 
            subprocess.run('. services/photo2cartoon/venv/bin/activate; python services/photo2cartoon/test.py --photo_path ' +file_path + ' --save_path ' + file_result_path,capture_output=False, shell=True)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        with open(file_result_path, 'rb') as fh:
            buf = BytesIO(fh.read())
            return send_file(
                buf,
                mimetype="image/png",
            )
    

