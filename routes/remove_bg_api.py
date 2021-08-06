"""The Endpoints to manage the BOOK_REQUESTS"""
import uuid
from flask import jsonify, abort, request, Blueprint
#remove bg

import os
import glob
from io import BytesIO
from urllib.parse import unquote_plus
from urllib.request import urlopen
from services.backgroundremover.bg import remove
from flask import send_file

REQUEST_API = Blueprint('remove_bg_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/api/remove-bg', methods=['GET', 'POST'])
def remove_bg_handler():
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
    alpha_matting = "a" in request.values
    print('==============',alpha_matting)
    af = request.values.get("af", type=int, default=240)
    ab = request.values.get("ab", type=int, default=10)
    ae = request.values.get("ae", type=int, default=10)
    az = request.values.get("az", type=int, default=1000)

    model = request.args.get("model", type=str, default="u2net")
    # model_path = os.environ.get(
    #     "U2NETP_PATH",
    #     os.path.expanduser(os.path.join("~", ".u2net")),
    # )
    # model_choices = [os.path.splitext(os.path.basename(x))[0] for x in set(glob.glob(model_path + "/*"))]
    # if len(model_choices) == 0:
    #     model_choices = ["u2net", "u2netp", "u2net_human_seg"]
    model_choices = ["u2net", "u2netp", "u2net_human_seg"]

    if model not in model_choices:
        return {"error": f"invalid query param 'model'. Available options are {model_choices}"}, 400

    try:
        return send_file(
            BytesIO(
                remove(
                    file_content,
                    model_name=model,
                    alpha_matting=alpha_matting,
                    alpha_matting_foreground_threshold=af,
                    alpha_matting_background_threshold=ab,
                    alpha_matting_erode_structure_size=ae,
                    alpha_matting_base_size=az,
                )
            ),
            mimetype="image/png",
        )
    except Exception as e:
        return {"error": "oops, something went wrong!"}, 500

