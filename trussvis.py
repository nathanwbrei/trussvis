#!/usr/bin/env python

from flask import Flask, request, render_template, session, url_for, redirect, escape
from flask_oauth import OAuth

import json
import sys
import argparse
import brain

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Create OAuth object
oauth = OAuth()
facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='109598425902918',
    consumer_secret='21599ff47fc62fcbee95a5b3453f5a63',
    request_token_params={'scope': 'email'}
)


@app.route('/user')
def stupid():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@app.route('/login2', methods=['GET', 'POST'])
def login2():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect('/user')
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


@app.route('/trussvis', methods=['POST'])
def trussvis():

    data = json.JSONDecoder().decode(request.data)
    print "> "+data['line']
    brain.dispatch(*data['line'].split())

    returndata = json.JSONEncoder().encode(brain.state)
    print "--> "+brain.state['msg']
    return returndata

@app.route("/trussvis/stress", methods=['POST'])
def stress_cmd():
    """Perform the complete static analysis"""

    state = State().from_json(request.data)
    from trussmath import statics
    stresses, deflections, reactions = statics(state)
    state['msg'] = "Calculated statics."
    return state.to_json()

@app.route("/trussvis/open", methods=['POST'])
def open_cmd():
    """Loads truss f from disk."""
    filename = json.JSONDecoder().decode(request.data)["filename"] 
    with (open("models/"+args[0])) as f:
        data = f.readlines()
        state = State().from_json(json.JSONDecoder().decode(data[0]))
        state.msg = "Opened truss at: " + args[0]


@register("save")
def save_cmd():
    """save f: Save truss under filename f."""
    
    state = State().from_json(request.data) 
    with (open("models/"+state.name, "w")) as f:
        f.write(state.to_json())
        state.msg = "Saved truss to: " + state.name 
    return state.to_json()

@app.route('/', methods=['GET'])
def mainpage():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
