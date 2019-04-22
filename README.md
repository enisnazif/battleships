# man.battleships


Your task is to implement a Bot to play a game of Battleships!


## Rules

- Your bot gets a maximum of 3 retries for placing ships in each game and
making shots on each turn. If after these retries you fail to return
valid ship placements / a valid shot, you either lose the game or lose the
chance to make a shot that round

- The maximum time allows to compute `place_ships` and `get_shot` is 300ms.
After this time, your move will time out and you will lose either the game or the
chance to make a shot that round

- Please play nicely! The code used to run the competition will be slightly different
(but still fully compatible with your bots) so don't get any funny ideas...

## Getting started

To implement your bot, your team must submit a class of Bot which
overrides the `place_ships` and `get_shot` methods.

## Game structure

A *match* consists of 100 *games* between two bots. Within each game
the following happens:

- Player 1 places their ships
- Player 2 places their ships
- Player 1/2 take alternating turns to shoot positions on the board of
their opponent.
- After each shot, your bot will receive a message indicating whether the last shot
hit / missed an enemy ship, and if so, what kind of ship was sunk
- The game ends when either player has 'sunk' all of their opponents ships

## Testing your bot

In order to test your bots, we have provided a script allowing you to
play `n` games between two Bots `p1` and `p2`. The usage of this script
is as follows:

python play_game -n [100] <p1> <p2>

Here, `p1` and `p2` are the string class names of the bots you wish to test.


## Submitting your bot

At the end of the competition, there will be be a competition.
In order to submit your bot, simply make a pull request to the `man/battleships/bots`
directory containing your implemented `Bot`.


Play fairly and Good Luck!

## Questions?

Find Enis, Alex or Doug