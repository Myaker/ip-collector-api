import datetime
import json
import os
from pathlib import Path

import my_env as env
from flask import Flask, request

initialized = False


def start():
    global initialized
    logs_pth = Path("logs")
    if not logs_pth.is_dir():
        os.mkdir('logs')
    start_up = open('logs/init.log', "a")
    start_up.write("\n> " + datetime.datetime.now().__str__() + " | " + os.uname().nodename.__str__() + " started.")
    start_up.close()
    initialized = True


def log_weird(meta):
    log_destination = open('logs/init.log', "a")
    log_destination.write("\n  " +
                          datetime.datetime.now().__str__() + " someone is posting shit:" + meta)
    log_destination.close()


app = Flask(__name__)


@app.route('/my_address', methods=['POST'])
def process_address():
    global initialized
    if not initialized:
        start()

    data = request.get_json(force=True, silent=False, cache=False)
    try:
        key: str = data["key"]
        host: str = data["host"]
        if key != env.KEY:
            raise Exception("WRONG KEY MFFF")

    except Exception as keyr:
        log_weird("\n    | Request:" + request.__str__() +
                  "\n    | Headers: " + request.headers.__str__() +
                  "    | Body: " + json.dumps(data) +
                  "\n    | Error: " + keyr.__str__())

    else:
        current_time = datetime.datetime.now()
        current_year = current_time.year.__str__()
        current_month = current_time.month.__str__()
        current_day = current_time.day.__str__()
        date_path = Path(current_year)
        if not date_path.is_dir():
            os.mkdir(current_year)
        date_path = Path(current_year + "/" + current_month)
        if not date_path.is_dir():
            os.mkdir(current_year + "/" + current_month)
        myday = open(current_year + "/" + current_month + "/" + current_day, "a")
        myday.write("\n> " + current_time.strftime("%H:%M:%S") + " | host:" + host)
    finally:
        return "Thanks!"


if __name__ == '__main__':
    app.run()
