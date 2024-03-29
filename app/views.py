import datetime
import json

import requests
from flask import render_template, redirect, request

from app import app

# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []

def get_key():
    asg = request.form.get('asg')
    print(asg)

def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                print(tx['asg'])
                content.append(tx)
        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)


@app.route('/index')
def index():
    return render_template('index.html',
                           title='Sistema '
                                 'de registro de aseguros',
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)

@app.route('/medical')
def medical():
    return render_template('medical.html',
                        title='Sistema de Aseguro | Centro Médico ',
                        posts=posts,
                        node_address=CONNECTED_NODE_ADDRESS,
                        readable_time=timestamp_to_string)

@app.route('/select')
def select():
    return render_template('select.html',
                        title='Selección de aseguradora',
                        posts=posts,
                        node_address=CONNECTED_NODE_ADDRESS,
                        readable_time=timestamp_to_string)

@app.route('/carrier')
def carrier():
    asg = request.form.get('asg')
    print(asg)
    fetch_posts()
    return render_template('carrier.html',
                        title='Sistema de Aseguro | Compañía Aseguradora ',
                        posts=posts,
                        node_address=CONNECTED_NODE_ADDRESS,
                        readable_time=timestamp_to_string)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    post_content = request.form["content"]
    author = request.form["author"]
    cedula = request.form["cedula"]
    nua = request.form["nua"]
    centro = request.form["centro"]
    curp = request.form["curp"]
    asg = request.form.get('asg')

    post_object = {
        'author': author,
        'content': post_content,
        'cedula': cedula,
        'nua' : nua,
        'centro' : centro,
        'asg' : asg,
        'curp' : curp,
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/medical')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
