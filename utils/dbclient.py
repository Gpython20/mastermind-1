#!/usr/bin/python

import configparser
import json
import os
import pymysql


class DBClient():
    connection = None
    config = configparser.RawConfigParser()

    def connect(self):
        try:
            if "MASTERMIND_PRODUCTION" in os.environ:
                print("Production config")
                self.config.read('config/production.cfg')
            else:
                print("Development config")
                self.config.read('config/development.cfg')
            print(self.config.sections())
            self.connection=pymysql.connect(host=self.config.get('mysql','host'),
                                            user=self.config.get('mysql','user'), 
                                            passwd=self.config.get('mysql','passwd'),
                                            db=self.config.get('mysql','db') )
        except Exception as e:
            print ("DBClient.connect: ",str(e))
            return False
        return True

    def close(self):
        self.connection.close
        return

    def insert_game(self, user, code):
        new_game_id = 0
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO games(userid, code) VALUES('{0}','{1}') ".format(user, code)
            cursor.execute (query)
            self.connection.commit()
            new_game_id = cursor.lastrowid
            cursor.close
        except Exception as e:
            print ("DBClient.insert_game: ",str(e))
            new_game_id = 0

        return new_game_id

    def get_game_data(self, gameid):
        response = {}
        try:
            cursor = self.connection.cursor()
            query = "SELECT code, plays, status FROM games WHERE id = {0}".format(gameid)
            cursor.execute(query)
            data = cursor.fetchall()
            if not data:
                return {}
            response = {"code":data[0][0], "plays":data[0][1], "status":data[0][2]}
        except Exception as e:
            print ("DBClient.get_game_data: ",str(e))

        return response

    def update_game_data(self, gameid, new_plays, status):
        updated = False
        try:
            cursor = self.connection.cursor()
            query = "UPDATE games SET plays = {0}, status={1} WHERE id = {2} ".format(new_plays, status, gameid)
            cursor.execute (query)
            self.connection.commit()
            cursor.close
            updated = True
        except Exception as e:
            print ("DBClient.update_game_data: ",str(e))

        return updated

    def insert_play(self, gameid, play, guess, key_pegs):
        inserted = False
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO plays(gameid, play,guess, key_pegs) VALUES({0},{1},'{2}','{3}') ".format(gameid, play, guess, key_pegs)
            cursor.execute (query)
            self.connection.commit()
            cursor.close
            inserted = True
        except Exception as e:
            print ("DBClient.insert_play: ",str(e))
        
        return inserted

    def get_game_history(self, gameid):
        response = []
        try:
            cursor = self.connection.cursor()
            query = "SELECT play, guess, key_pegs FROM plays WHERE gameid = {0}".format(gameid)
            cursor.execute(query)
            data = cursor.fetchall()
            for row in data:
                response.append( {"play":row[0], "guess":json.loads(row[1]), "key_pegs":json.loads(row[2])} )
        except Exception as e:
            print ("DBClient.get_game_history: ",str(e))
            response = {"Error":"Error reading game history"}

        return response