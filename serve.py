from flask import Flask, request
from flask_json import FlaskJSON, JsonError, as_json
from werkzeug.utils import secure_filename
from teco_twitterbot.twitter_bot import call_teco
from gensim.models import KeyedVectors
from teco_config.load_config import *
from proverb_selector.sel_utils.file_manager import read_write_obj_file

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
APP_ROOT = "./"
app.config["APPLICATION_ROOT"] = APP_ROOT
app.config["UPLOAD_FOLDER"] = "files/"

json_app = FlaskJSON(app)

config = {}

"""
@app.before_first_request
def before_first_request():
    app.logger.info("before_first_request")
    load_config()
"""


@as_json
@app.route("/predict_json", methods=["POST"])
def predict_json():

    data = request.get_json()
    if (data.get("type") != "text") or ("content" not in data):
        output = invalid_request_error(None)
        return output
    content = data["content"]
    try:
        output = make_request_teco(content)
        return output
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(e)
        return generate_failure_response(
            status=404,
            code="elg.service.internalError",
            text=None,
            params=None,
            detail=str(e),
        )


@json_app.invalid_json_error
def invalid_request_error(e):
    """Generates a valid ELG "failure" response if the request cannot be parsed"""
    raise JsonError(
        status_=400,
        failure={
            "errors": [
                {"code": "elg.request.invalid", "text": "Invalid request message"}
            ]
        },
    )


def make_request_teco(text):

    headline, generated = call_teco(
        text,
        config["all_expressions"],
        config["model"],
        config["dict_forms_labels"],
        config["dict_lemmas_labels"],
        config["configs"],
        config["gen_method"],
    )
    if generated:
        return prepare_output_format(generated)
    else:
        return generate_failure_response(
            status=404,
            code="elg.service.internalError",
            text=None,
            params=None,
            detail=None,
        )


def prepare_output_format(prediction):
    list_options = list()
    list_options.append({"content": prediction[1], "score": round(prediction[2][0], 3)})
    return {"response": {"type": "texts", "texts": list_options}}


def generate_failure_response(status, code, text, params, detail):
    error = {}
    if code:
        error["code"] = code
    if text:
        error["text"] = text
    if params:
        error["params"] = params
    if detail:
        error["detail"] = {"message": detail}

    raise JsonError(status_=status, failure={"errors": [error]})


def load_config_teco():
    file_paths = load_config()
    print("Expressions", file_paths[EXPRESSIONS])
    all_expressions = read_write_obj_file(1, None, file_paths[EXPRESSIONS])
    print("Model", file_paths[EMBEDDINGS])
    model = KeyedVectors.load(file_paths[EMBEDDINGS])
    print("Lexicon", file_paths[LEXICON])
    dict_forms_labels = read_write_obj_file(1, None, file_paths[LEXICON])

    configs = [
        file_paths[FIRST_SEL],
        int(file_paths[N_FIRST_SEL]),
        file_paths[FINAL_SEL],
    ]

    gen_method = file_paths[GEN_METHOD]
    print("Gen method", gen_method)

    dict_lemmas_labels = dict_forms_to_lemmas_label(dict_forms_labels)

    config["all_expressions"] = all_expressions
    config["model"] = model
    config["dict_forms_labels"] = dict_forms_labels
    config["dict_lemmas_labels"] = dict_lemmas_labels
    config["configs"] = configs
    config["gen_method"] = gen_method


def dict_forms_to_lemmas_label(dict_forms_labels):
    dict_lemmas_labels = {}
    for form in dict_forms_labels:
        for entry in dict_forms_labels[form]:
            if entry[1] not in dict_lemmas_labels:
                dict_lemmas_labels[entry[1]] = []
            dict_lemmas_labels[entry[1]].append(entry)
    return dict_lemmas_labels


if __name__ == "__main__":
    load_config_teco()
    app.run(host="0.0.0.0", port=8866)
