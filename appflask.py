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

from utils.game import Game

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
    game = Game()
    new_game_id = game.new_game(userid)
    return json.dumps(new_game_id)

@app.route('/guess/<string:gameid>/<string:pos_1>/<string:pos_2>/<string:pos_3>/<string:pos_4>',methods = ['GET'])
def guess(gameid, pos_1, pos_2, pos_3, pos_4):
    guess = {"pos_1":int(pos_1), "pos_2": int(pos_2), "pos_3":int(pos_3), "pos_4":int(pos_4)}
    game = Game()
    feedback = game.guess(gameid, guess)
    return json.dumps(feedback)