#!/usr/bin/python

import pymysql

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
        query = "select code, plays from games where id = {0}".format(gameid)
        cursor.execute(query)
        data = cursor.fetchall()
        if not data:
            return {}
        response = {"code":data[0][0], "plays":data[0][1]}

        return response