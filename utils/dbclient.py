#!/usr/bin/python

import pymysql
import json

class DBClient():

    def connect(self):
        self.connection=pymysql.connect(host="localhost",user="mastermind", passwd="M4st3rmind",db="mastermind" )
        return

    def close(self):
        self.connection.close
        return

    def insert_game(self, user, code):
        cursor = self.connection.cursor()
        query = "INSERT INTO games(userid, code) VALUES('{0}','{1}') ".format(user, code)
        cursor.execute (query)
        self.connection.commit()
        new_game_id = cursor.lastrowid
        cursor.close
        return new_game_id

    def get_game_data(self, gameid):
        response = {}
        cursor = self.connection.cursor()
        query = "SELECT code, plays, status FROM games WHERE id = {0}".format(gameid)
        cursor.execute(query)
        data = cursor.fetchall()
        if not data:
            return {}
        response = {"code":data[0][0], "plays":data[0][1], "status":data[0][2]}

        return response

    def update_game_data(self, gameid, new_plays, status):
        cursor = self.connection.cursor()
        query = "UPDATE games SET plays = {0}, status={1} WHERE id = {2} ".format(new_plays, status, gameid)
        cursor.execute (query)
        self.connection.commit()
        cursor.close
        return 

    def insert_play(self, gameid, play, guess, key_pegs):
        cursor = self.connection.cursor()
        query = "INSERT INTO plays(gameid, play,guess, key_pegs) VALUES({0},{1},'{2}','{3}') ".format(gameid, play, guess, key_pegs)
        cursor.execute (query)
        self.connection.commit()
        cursor.close
        return

    def get_game_history(self, gameid):
        response = []
        cursor = self.connection.cursor()
        query = "SELECT play, guess, key_pegs FROM plays WHERE gameid = {0}".format(gameid)
        cursor.execute(query)
        data = cursor.fetchall()
        for row in data:
            response.append( {"play":row[0], "guess":json.loads(row[1]), "key_pegs":json.loads(row[2])} )

        return response