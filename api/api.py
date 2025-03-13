from gevent.pywsgi import WSGIServer
from flask import Flask, request, jsonify
from request_ticker_counter.ticker_counter_executer import get_yesterday_str, read_result_from_file
import config

app = Flask(__name__)


def generate_html_table(column_names, data: dict, title: str = None):
    html = "<table border='1'>\n"

    if title:
        html += f"  <caption><strong>{title}</strong></caption>\n"

    html += "  <tr>\n"
    for column in column_names:
        html += f"    <th>{column}</th>\n"
    html += "  </tr>\n"

    for key, value in data.items():
        html += "  <tr>\n"
        html += f"    <td>{key}</td>\n"
        html += f"    <td>{value}</td>\n"
        html += "  </tr>\n"

    html += "</table>"

    return html


def get_yesterday_data() -> dict:
    yesterday_str = get_yesterday_str()
    data = read_result_from_file(yesterday_str)
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
    return sorted_data


@app.route("/protected")
def protected_route():
    api_key = request.args.get("api_key")

    if api_key != config.API_KEY:
        return jsonify({"error": "Unauthorized: Invalid API key"}), 401

    try:
        yesterday_data = get_yesterday_data()
        return generate_html_table(
            column_names= ["company_name", "occurrence"],
            data = yesterday_data,
            title = "Alberts wallstreet bets"
        )
    except Exception:
        return "FAILED TO LOAD RESULT"


@app.route('/')
def index():
    return "Hello, HTTP!"

if __name__ == "__main__":
    # Host and port for the HTTP server
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
