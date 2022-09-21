from flask import Flask
from flask import make_response
from waitress import serve

app = Flask(__name__)


@app.route("/api/v1/hello-world-15")
def printing():
    return make_response("hello world 15", 200)


if __name__ == "__main__":
    serve(app, host='127.0.0.1', port=5000)
    app.run(debug=True)


