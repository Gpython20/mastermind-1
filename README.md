# Mastermind
Master Mind game API

This is a very simple API for the game [Mastermind] (https://en.wikipedia.org/wiki/Mastermind_(board_game)). It has been implemented with GET http methods so it can be easly tested on any web browser. The game functions with 

The whole game is based in 3 functions:

1.- /newgame/(userid)
This function creates a new game on the database with the initial code asociated with a userid 

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

Example: {'key_pegs':[1,0,0], 'plays': 3, 'status': 0}

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
pip install requirments.txt
````

Run
```
python app.py
`````

## Limitations
This is a simple implementation so its several limitations for example the key of the games ids on the database is an int so thats the number of games can be played. This can be improved.
