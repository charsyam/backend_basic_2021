from flask import Flask

import os

app = Flask(__name__)


@app.route('/')
def hello():
    name = os.environ["APPNAME"]
    return f"Hello World! - {name}"

if __name__ == '__main__':
    app.run("0.0.0.0")
