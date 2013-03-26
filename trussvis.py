#!/usr/bin/env python

from flask import Flask, request, render_template
import json
import sys
import argparse
import brain

app = Flask(__name__)

@app.route('/trussvis', methods=['POST'])
def trussvis():

    data = json.JSONDecoder().decode(request.data)
    print "> "+data['line']
    brain.dispatch(*data['line'].split())

    returndata = json.JSONEncoder().encode(brain.state)
    print "--> "+brain.state['msg']
    return returndata


@app.route('/', methods=['GET'])
def mainpage():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()