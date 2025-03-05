# app.py 
print('server starting....')

from flask import Flask, jsonify, request, send_from_directory


from gevent import monkey 
monkey.patch_all() # handle multiple requests at the same time
import traceback
app = Flask(__name__)


def JSON_RESPONSE(message=None, details=None, action=None, error=False, online_mode=False):
    if error == True:
        status_code = 400
    else:
        # Fix the logic - default to 200 when not an error
        status_code = error
    
    response = {"status": "error" if error else "success", "error": {"message": message, "details": details, "action": action}, "online_mode": online_mode}
    return jsonify(response), status_code



@app.route("/speed_test_POST", methods=["POST"])
def speed_test_POST():
    try:
        recived_data = request.get_json()
        invite_code = recived_data.get('invite_code', None)
        return JSON_RESPONSE(details={"invite_code": invite_code})
    except Exception as e:
        app.logger.error(f"Error in speed_test_POST: {str(e)}")
        app.logger.error(traceback.format_exc())
        return JSON_RESPONSE(message="Internal server error", error=True)

@app.route("/speed_test_GET", methods=["GET"])
def speed_test_GET():
    try:
        invite_code = request.args.get('invite_code', None)
        return JSON_RESPONSE(details={"invite_code": invite_code})
    except Exception as e:
        app.logger.error(f"Error in speed_test_GET: {str(e)}")
        app.logger.error(traceback.format_exc())
        return JSON_RESPONSE(message="Internal server error", error=True)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)

    