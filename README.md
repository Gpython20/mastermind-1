# Mastermind
Master Mind game API

This is a very simple API for the game Mastermind (https://en.wikipedia.org/wiki/Mastermind_(board_game)) on its basic version 4 spaces, 6 colors 8 chances. It has been implemented with GET http methods so it can be easly tested on any web browser.  

The whole game is based in 3 functions:

1.- /newgame/(userid)
This function creates a new game on the database with the initial code asociated with a userid. Returns a JSON object with the gameid or in case or error the function returns a gameid = 0:

2.- /guess/(pos_1)/(pos_2)/(pos_3)/(pos_4)
With this function the user sends its guess for the code where pos_X is the code for the color on the X position. The color codes are:

    1 = Red
    2 = Yellow
    3 = Blue
    4 = Orange
    5 = Green
    6 = Violet

The function returns a JSON object containing the key pegs as a list, the number of plays this had and the status of the game. The game status codes are:

    0 = Game open
    1 = Game won
    2 = Game lost 

Example of a response: {'key_pegs':[1,0,0], 'plays': 3, 'status': 0}

In case of error the function returns a JSON object with the error description. Example: {"Error": "Error getting game data"}

Once the game has won or reach the number of max guesses the game can not be played anymore and the function will return the last feedback.

3.- /history/(gameid)
This function returns all the history of the game as a JSON object. Each play will be an object of a list and each play will have the play number, the guess sent and the key pegs generated.

[{"play":1, "guess":{"pos_1":2, "pos_1":3, "pos_1":4, "pos_1":5}, "key_pegs":[0]},
{"play":2, "guess":{"pos_1":2, "pos_1":3, "pos_1":5, "pos_1":5}, "key_pegs":[0,0]}]

## Run
Clone the repo:

```
git clone https://github.com/rodulforg/mastermind.git
````

Create Virtual enviroment

```
virtualenv -p python3 venv
````

Activate the virtual environment

````
source venv/bin/activate
````

Install requirements

```
pip install -r requirements.txt
````

Run

```
python app.py
`````
By defaut the server runs on port 8090, but can be specified as a parameter. Example: python app.py 80

## Database
The database has been implemented in MySQL. A file containing the database structure is included as mastermind.sql

## Configuration
The configuration is read from the files development.cfg and production.cfg. If the environmental variable "MASTERMIND_PRODUCTION" exists it will read the production file otherwise it will use the development configuration.

## Limitations
This is a simple implementation so its several limitations for example the key of the games ids on the database is an int so thats the number of games can be played. This can be improved.

The API is designed for basic gameplay 4 spaces, 6 colors and 8 chances but can be easly modified for other play options.

Another limitation is that no security has been implementated.
