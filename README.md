# battleships :ship:


Your task is to implement a Bot to play a game of [Battleships](https://www.thesprucecrafts.com/the-basic-rules-of-battleship-411069)!

In a game of battleships, each player has a 10 x 10 board on which they place 5 different types of ship.

The aim of the game is to shoot all of your opponents ships before they shoot yours.



## Getting started

After cloning this repo, to get started, run:

`python -m venv virtualenv` (optional but recommended)

`source virtualenv/bin/activate`

`pip install -r requirements.txt`

To implement your bot, your team must submit an implementation of `Bot` which
overrides the `place_ships` and `get_shot` methods. You can see examples of implemented bots
under `man.battleships/bots`. `SampleBot.py` is a good place to start.

## Game structure

Within each *game* between two bots, the following happens:

- Player 1 places their ships
- Player 2 places their ships
- Player 1/2 take alternating turns to shoot positions on the board of
their opponent.
- After each shot, your bot will receive a `dict` of information indicating whether the last shot
hit / missed an enemy ship, sunk an enemy ship, and if so, which ship it was, or an exception if the shot failed for some reason.
- The game ends when either player has 'sunk' all of their opponents ships

## Testing your bot

### Command line

In order to test your bots, we have provided a script allowing you to
play `n` games between two Bots `p1` and `p2` present in the `bots` directory. The usage of this script
is as follows:

`python play_game -n [100] <p1> <p2>`

Here, `p1` and `p2` are the string class names of the bots you wish to test.

### Visualising games

Alternatively, you may wish to visualise games between two bots. To run the game visualiser and backend, run:

`./run_all.sh` (or `run_all.bat` on windows)

You can then navigate to `localhost:8000` to play a game between any of the bots present in `man.battleships/bots`

## Rules
- Your bot gets a maximum of 3 retries for placing ships in each game and
making shots on each turn. If after these retries you fail to return
valid ship placements / a valid shot, you either lose the game or lose the
chance to make a shot that round

- The maximum time allowed to compute `place_ships` and `get_shot` each round is 100ms.
After this time, your move will time out and you will lose either the game (if `place_ships` has timed out) or the
chance to make a shot that round (if `get_shot` has timed out)

- Please play nicely! any obvious attempts to break the game engine will be disqualified

## Submitting your bot

In order to submit your bot, simply make a pull request to `man.battleships` containing your
implemented `Bot` in the `man.battleships/bots` directory .
Ensure that your Python file and implemented `Bot` class have the same name.

Good Luck!

## Questions?

Find Enis, Alex or Doug
