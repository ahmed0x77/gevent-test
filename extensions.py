
import logging
import sys
import colorama
from flask_caching import Cache
from flask import Flask, jsonify, request, send_from_directory
import os
import binascii
import warnings

from gevent import monkey 
monkey.patch_all() # handle multiple requests at the same time

app_cache = False

app = Flask(__name__)

warnings.filterwarnings("ignore", message=".*CACHE_TYPE is set to null, caching is effectively disabled.*") # HIDE CACHE WARNING ABOUT ITS DISABLED
cache = Cache()
if app_cache:
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
else:
    cache.init_app(app, config={'CACHE_TYPE': 'null'})


#-- this is to make the cache remember different body for the api
def make_cache_key(*args, **kwargs): 
    # Create a cache key based on the request path and its body 
    request_data = request.get_data(as_text=True)
    return request.path + request_data

app.secret_key = binascii.hexlify(os.urandom(24)).decode() #مش عارف هو مهم اوي ولا لا


# @app.before_request
# def log_request_info():
#     logging.info(f"Endpoint called: {request.endpoint}, Method: {request.method}, Path: {request.path}")

@app.route('/favicon.ico') #this fix that when calling
def favicon():
    return send_from_directory('imgs', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

#------ Show a better error message in the console ------
import traceback
from colorama import Fore, Style
colorama.init(autoreset=True)
@app.errorhandler(Exception)
def handle_user_code_exception(e):
    # Extract the traceback frames
    tb_list = traceback.extract_tb(e.__traceback__)
    short_trace = Fore.YELLOW + "*** Traceback (most recent call last) ***\n" + Style.RESET_ALL
    for frame in tb_list:
        if not "Programs\\Python" in frame.filename and not "lib\\" in frame.filename:
            short_trace += Fore.CYAN + f'File "{frame.filename.replace(sys.path[0], "")}", line {frame.lineno}, in {frame.name}\n' + Style.RESET_ALL
            if frame.line:
                short_trace += Fore.GREEN + f"   {frame.line.strip()}\n" + Style.RESET_ALL
    short_trace += Fore.RED + f"\n{type(e).__name__}: {e}\n" + Style.RESET_ALL
    logging.error(short_trace)
    return jsonify({"error": "Something went wrong"}), 500

#### other way of hide unnessary error #####
# logging.getLogger('werkzeug').setLevel(logging.ERROR)
# # Remove or adjust the traceback limit so we can get one frame's info
# sys.tracebacklimit = 1  # Shows only the last frame