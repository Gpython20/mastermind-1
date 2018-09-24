#!/usr/bin/python
import json

from flask_cors import CORS
from flask import send_from_directory, url_for
from flask import Flask, jsonify, session
from flask import (make_response, 
                request,
                current_app, 
                render_template, 
                redirect,
                flash,
                session)

from utils.dbclient import DBClient

app = Flask(__name__)
CORS(app)
app.debug = True    
app.use_reloader = True
app.config['SECRET_KEY'] = 'mJhjk2FMdmMQVRK9B3rxcrw41A4eOBDZ'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def root():
    return "Mastermind API"

@app.route('/newgame/<string:userid>',methods = ['GET'])
def newgame(userid):
    db_client = DBClient()
    db_client.connect()
    gameid = db_client.insert_game(userid)
    db_client.close()
    return json.dumps({"gameid": gameid})