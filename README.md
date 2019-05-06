# man.battleships


Your task is to implement a Bot to play a game of Battleships!

In a game of battleships, each player has a 10 x 10 board on which they place 5 different types of ship.

The aim of the game is to shoot all of your opponents ships before they shoot yours.



## Getting started

To install, run:

`python -m venv virtualenv`

`source virtualenv/bin/activate`

`pip install -r requirements.txt`

`python setup.py install.py`

To implement your bot, your team must submit an implementation of `Bot` which
overrides the `place_ships` and `get_shot` methods. You can see examples of implemented bots
under `man/battleships/bots`

## Game structure

A *match* consists of 100 *games* between two bots. Within each game
the following happens:

- Player 1 places their ships
- Player 2 places their ships
- Player 1/2 take alternating turns to shoot positions on the board of
their opponent.
- After each shot, your bot will receive a message indicating whether the last shot
hit / missed an enemy ship, or an exception if the shot failed for some reason.
- The game ends when either player has 'sunk' all of their opponents ships

## Testing your bot

In order to test your bots, we have provided a script allowing you to
play `n` games between two Bots `p1` and `p2` present in the `bots` directory. The usage of this script
is as follows:

`python play_game -n [100] <p1> <p2>`

Here, `p1` and `p2` are the string class names of the bots you wish to test.

## Rules
- Your bot gets a maximum of 3 retries for placing ships in each game and
making shots on each turn. If after these retries you fail to return
valid ship placements / a valid shot, you either lose the game or lose the
chance to make a shot that round

- The maximum time allows to compute `place_ships` and `get_shot` is 300ms.
After this time, your move will time out and you will lose either the game or the
chance to make a shot that round

- Please play nicely! The code used to run the competition will be slightly different
(but still fully compatible with your bots)

## Submitting your bot

In order to submit your bot, simply make a pull request to `man.battleships` containing your
implemented `Bot` in the `man/battleships/bots` directory containing your implemented `Bot`.
Ensure that your python file and implemented `Bot` class have the same name.

Good Luck!

## Questions?

Find Enis, Alex or Doug
