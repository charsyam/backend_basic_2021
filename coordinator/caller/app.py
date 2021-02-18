from flask import Flask

import json
import os
import random

from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError
from kazoo.exceptions import NodeExistsError

import requests

app = Flask(__name__)

ZK_PATH = "/service/callee/"
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

current_nodes = []


@zk.ChildrenWatch(ZK_PATH)
def my_func(children):
    nodes = []
    for child in children:
        data, stat = zk.get(f"{ZK_PATH}{child}")
        nodes.append(data.decode("utf-8"))

    global current_nodes
    current_nodes = nodes


@app.route('/')
def hello():
    global current_nodes
    size = len(current_nodes)

    idx = random.randrange(0, size)
    host = current_nodes[idx]

    url = f"http://{host}/api/v1/name"
    ret = requests.get(url)
    print(ret.text)
    msg = json.loads(ret.text) 
    name = msg["data"]["host"] 
    return f"Hello World! from {host}"

@app.route('/list')
def list():
    global current_nodes
    return str(current_nodes)


if __name__ == '__main__':
    app.run("0.0.0.0")
