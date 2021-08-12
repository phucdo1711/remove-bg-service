"""The Endpoints to manage the BOOK_REQUESTS"""
from flask import request, Blueprint

from io import BytesIO
from urllib.parse import unquote_plus
from urllib.request import urlopen
from services.style_transfer.neural_style.neural_style import stylize
from flask import send_file

REQUEST_API = Blueprint('style_transfer_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/api/style-transfer', methods=['GET', 'POST'])
def style_transfer_handler():
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

    model = request.args.get("model", type=str, default="candy")
    # model_path = os.environ.get(
    #     "U2NETP_PATH",
    #     os.path.expanduser(os.path.join("~", ".u2net")),
    # )
    # model_choices = [os.path.splitext(os.path.basename(x))[0] for x in set(glob.glob(model_path + "/*"))]
    # if len(model_choices) == 0:
    #     model_choices = ["u2net", "u2netp", "u2net_human_seg"]
    model_choices = ['candy', 'mosaic', 'udnie', 'rain-princess', 'dog', 'mona-lisa','girl_with_pearl_earring', 'great_wave_off']

    if model not in model_choices:
        return {"error": f"invalid query param 'model'. Available options are {model_choices}"}, 400
    try:
        return send_file(
            BytesIO(
                stylize(
                    image_data= file_content,
                    model=model,
                )
            ),
            mimetype="image/png",
        )
    except Exception as e:
        return {"error": "oops, something went wrong!"}, 500

