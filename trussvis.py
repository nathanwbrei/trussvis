#!/usr/bin/env python

from flask import Flask, request, render_template
import json
import sys
import argparse

app = Flask(__name__)

@app.route('/trussvis', methods=['POST'])
def trussvis():

    data = json.JSONDecoder().decode(request.data)
    print "received "+str(data)

    returndata = json.JSONEncoder().encode({"result":"Noop `"+data['line']+"` successful.", "members":33, "interfaces":44})
    print "returning "+returndata
    return returndata


@app.route('/', methods=['GET'])
def mainpage():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()