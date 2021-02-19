import json
import os

from flask import Flask
from flask import Response
from flask import jsonify

from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError
from kazoo.exceptions import NodeExistsError


app = Flask(__name__)

ZK_PATH = "/service/leader/"
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()


FOLLOWER = "Follower"
LEADER = "leader"

role = FOLLOWER


def register_as_callee(bind_address):
    zk.create(ZK_PATH, bind_address.encode('utf-8'), sequence=True, ephemeral=True, makepath=True)


@zk.ChildrenWatch(ZK_PATH)
def my_func(children):
    if len(children) == 0:
        role = LEADER
        return

    nodes = []
    for child in children:
        data, stat = zk.get(f"{ZK_PATH}{child}")
        print("child: ", child, " ", data.decode("utf-8"))
        nodes.append(data.decode("utf-8"))

    sorted_nodes = sorted(nodes)
    host = os.environ["BIND"]

    if sorted_nodes[0] == host:
        role = LEADER
    else:
        role = FOLLOWER

    print(f"{host} role => {role}")


@app.route('/api/v1/name')
def get_name():
    host = os.environ["BIND"]
    msg = {"data": {"host": host, "role": role}}
    return Response(response=json.dumps(msg),
                    status=200,
                    mimetype='application/json')


if __name__ == '__main__':
    bind_address = os.environ["BIND"]
    parts = bind_address.split(':')
    register_as_callee(bind_address)
    app.run(host=parts[0], port=int(parts[1]))
