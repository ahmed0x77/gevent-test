# app.py 
print('server starting....')

from flask import Flask, jsonify, request, send_from_directory


from gevent import monkey 
monkey.patch_all() # handle multiple requests at the same time

app = Flask(__name__)


def JSON_RESPONSE(message=None, details=None, action=None, error=False, online_mode=False):
    if error == True:
        status_code = 400
    else:
        status_code = error

    response = {"status": "error", "error": {"message": message, "details": details, "action": action}, "online_mode": online_mode}
    return jsonify(response), status_code


@app.route("/speed_test_POST", methods=["POST"])
def speed_test_POST():
    recived_data = request.get_json()
    invite_code = recived_data.get('invite_code', None)
    return JSON_RESPONSE(details={"invite_code": invite_code})

@app.route("/speed_test_GET", methods=["GET"])
def speed_test_GET():
    invite_code = request.args.get('invite_code', None)
    return JSON_RESPONSE(details={"invite_code": invite_code})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)

    