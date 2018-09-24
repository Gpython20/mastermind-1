#!/usr/bin/python

import pymysql

class DBClient():

    def connect(self):
        self.connection=pymysql.connect(host="localhost",user="mastermind", passwd="M4st3rmind",db="mastermind" )
        return

    def close(self):
        self.connection.close
        return

    def insert_game(self, user):
        cursor = self.connection.cursor ()
        query = "INSERT INTO games(userid) VALUES('{0}') ".format(user)
        cursor.execute (query)
        self.connection.commit()
        new_game_id = cursor.lastrowid
        print ("New Game:", new_game_id)
        cursor.close
        return new_game_id