#!/usr/bin/python
import json
from .dbclient import DBClient
from random import randint

class Game():

    # Color codes
    # 1 = Red
    # 2 = Yellow
    # 3 = Blue
    # 4 = Orange
    # 5 = Green
    # 6 = Violet

    def create_code(self):
        code_position_list = ["pos_1", "pos_2","pos_3","pos_4"]
        code = {}
        for position in code_position_list:
            code[position] = randint(1, 6)
        return code

    def get_game_data(self, gameid):
        db_client = DBClient()
        db_client.connect()
        game_data = db_client.get_game_data(gameid)
        db_client.close()
        return game_data

    def new_game(self, userid):
        db_client = DBClient()
        db_client.connect()
        new_code = self.create_code()
        gameid = db_client.insert_game(userid, json.dumps(new_code) )
        db_client.close()
        return {"gameid": gameid}

    def guess(self, gameid, guess):
        game_data = self.get_game_data(gameid)
        code = json.loads(game_data['code'])
        positions = list(code.keys())
        key_pegs = []
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

        return {'key_pegs':key_pegs}


