#!/usr/bin/python
import json
from .dbclient import DBClient
from random import randint

MAX_RETRIES = 8

class Game():

    # Color codes
    # 1 = Red
    # 2 = Yellow
    # 3 = Blue
    # 4 = Orange
    # 5 = Green
    # 6 = Violet

    # Status codes
    # 0 = Game open
    # 1 = Game won
    # 2 = Game lost

    def create_code(self):
        code_position_list = ["pos_1", "pos_2","pos_3","pos_4"]
        code = {}
        for position in code_position_list:
            code[position] = randint(1, 6)
        return code

    def get_game_data(self, gameid):
        db_client = DBClient()
        game_data = {}
        if db_client.connect():
            game_data = db_client.get_game_data(gameid)
            db_client.close()
        else:
            print ("Error: Can not connect to DB")
        return game_data

    def update_game_data(self, gameid, plays, status):
        updated = False
        db_client = DBClient()
        if db_client.connect():
            updated = db_client.update_game_data(gameid, plays, status)
            db_client.close()
        else:
            print ("Error: Can not connect to DB")
        return updated

    def new_game(self, userid):
        db_client = DBClient()
        gameid = 0
        if db_client.connect():
            new_code = self.create_code()
            gameid = db_client.insert_game(userid, json.dumps(new_code) )
            db_client.close()
        else:
            print ("Error: Can not connect to DB")
        return {"gameid": gameid}

    def save_play(self, gameid, play, guess, key_pegs):
        saved = False
        db_client = DBClient()
        if db_client.connect():
            saved = db_client.insert_play(gameid, play, guess, key_pegs)
            db_client.close()
        else:
            print ("Error: Can not connect to DB")
        return saved

    def guess(self, gameid, guess):
        key_pegs = []
        response = {}

        game_data = self.get_game_data(gameid)
        if game_data:
            
            #First we check if the game still can be played otherwise we return the last data
            #Logic to not allow a game to be played when the game has ended should be on the client side
            if game_data['plays'] ==  MAX_RETRIES or game_data['status'] != 0:
                return {'key_pegs':key_pegs, 'plays':game_data['plays'], 'status':game_data['status']}

            #We get the guess results in the key_pegs
            code = json.loads(game_data['code'])
            positions = list(code.keys())
            code_not_exact_coincidences = []
            guess_not_exact_coincidences = []

            #First we get exact coincidences (place and color)
            for position in positions:
                if code[position] == guess[position]:
                    key_pegs.append(1)
                else:
                    code_not_exact_coincidences.append(code[position])
                    guess_not_exact_coincidences.append(guess[position])

            #Then we search in the remaining positions for color matches
            for color in guess_not_exact_coincidences:
                if color in code_not_exact_coincidences:
                    key_pegs.append(0)
                    code_not_exact_coincidences.remove(color)

            #Update game status
            new_play = game_data['plays'] + 1
            new_status = 0 

            #We check if all the positions have been guesses
            if sum(key_pegs) == 4:
                new_status = 1
            else:
                #In the last play we update the status
                if new_play == MAX_RETRIES:
                    new_status = 2

            # We update the game status and save the play for game history
            if self.update_game_data(gameid, new_play, new_status):
                if self.save_play(gameid, new_play, json.dumps(guess), json.dumps(key_pegs) ):
                    response = {'key_pegs':key_pegs, 'plays': new_play, 'status': new_status}
                else:
                    response = {"Error": "Error saving play"}
            else:
                response = {"Error": "Error updating game data"}

            
        else:
            response = {"Error": "Error getting game data"}

        return response

    def history(self, gameid):
        history = []
        db_client = DBClient()
        if db_client.connect():
            history = db_client.get_game_history(gameid)
            db_client.close()
        else:
            print ("Error: Can not connect to DB")
        return history


