import importlib
import logging

from man.battleships.config import MAX_SHOT_TIME, MAX_PLACE_TIME
from man.battleships.exceptions import (
    InvalidShipPlacementException,
    InvalidShotException,
    MaxRetriesExceededException,
    NotAPointError,
)
from man.battleships.game_types import Point, Board
from man.battleships.game_types.Ship import ships_to_place
from man.battleships.utils import retry

logging.basicConfig(filename='games.log', level=logging.DEBUG)


# TODO: Timeout!
# TODO: Fix bug with timeout
# TODO: Fix need to constantly python setup.py install
# TODO: Update ship types
# TODO: Test game - all cases

class Game:
    def __init__(self, players, game_id):

        # Set game_id
        self.game_id = game_id

        # Create boards
        self.first_player_board = Board()
        self.second_player_board = Board()

        # Import the players
        bots_path = "man.battleships.bots"
        self.player_bots = [
            getattr(importlib.reload(importlib.import_module(f"{bots_path}.{p}")), p)() for p in players
        ]

        self.first_player = self.player_bots[0]
        self.second_player = self.player_bots[1]

    def _check_valid_placements(self, p1_placements, p2_placements):
        if not p1_placements and p2_placements:
            logging.error(f'{self.first_player.name} screwed up ship placement - {self.second_player.name} wins!')
            winner = self.second_player.name
        elif not p2_placements and p1_placements:
            logging.error(f'{self.second_player.name} screwed up ship placement - {self.first_player.name} wins!')
            winner = self.first_player.name
        elif not p1_placements and not p2_placements:
            logging.error('Both players screwed up ship placement - no one wins!')
            winner = None
        else:
            logging.info('Ship placements were both valid - continuing the game!')
            winner = None

        return winner

    def play_game(self):

        logging.info(f'Starting game {self.game_id} between {self.first_player.name} and {self.second_player.name}')

        # Perform ship placement (Keep retrying until we get a correct placement). If we don't, end the game here
        try:
            p1_placements = self._place_ships(
                self.first_player, self.first_player_board
            )
        except MaxRetriesExceededException:
            p1_placements = []

        try:
            p2_placements = self._place_ships(
                self.second_player, self.second_player_board
            )
        except MaxRetriesExceededException:
            p2_placements = []

        # Check to see if someone screwed up ship placement
        early_winner = self._check_valid_placements(p1_placements, p2_placements, )

        # If someone screwed up placement, end the game early
        if early_winner:
            return {
                "id": self.game_id,
                "p1_name": self.first_player.name,
                "p2_name": self.second_player.name,
                "p1_ship_placements": [],
                "p2_ship_placements": [],
                "p1_shots": [],
                "p2_shots": [],
                "winner": early_winner
            }

        p1_shots = []
        p2_shots = []

        # Game loop - get shots until a player wins
        while True:

            # Get first player shot
            try:
                p1_shot, p1_is_hit = self._do_shot(self.first_player, self.second_player_board)
                p1_shots.append(p1_shot)
                logging.info(f'{self.first_player.name} shot at {p1_shot} and {"hit" if p1_is_hit else "missed"}')
                self.first_player.last_shot_status = (p1_shot, p1_is_hit)
            except MaxRetriesExceededException as e:
                self.first_player.last_shot_status = (None, e)

            if self.second_player_board.is_board_lost():
                winner = self.first_player.name
                break

            # Get second player shot
            try:
                p2_shot, p2_is_hit = self._do_shot(self.second_player, self.first_player_board)
                p2_shots.append(p2_shot)
                logging.info(f'{self.second_player.name} shot at {p2_shot} and {"hit" if p2_is_hit else "missed"}')
                self.second_player.last_shot_status = (p2_shot, p2_is_hit)
            except MaxRetriesExceededException:
                self.second_player.last_shot_status = (None, e)

            if self.first_player_board.is_board_lost():
                winner = self.second_player.name
                break

        logging.info(f'{winner} wins!')

        # Return completed game data
        game_data = {
            "id": self.game_id,
            "p1_name": self.first_player.name,
            "p2_name": self.second_player.name,
            "p1_ship_placements": list(p1_placements),
            "p2_ship_placements": list(p2_placements),
            "p1_shots": list(p1_shots),
            "p2_shots": list(p2_shots),
            "winner": winner,
        }

        return game_data

    @retry(InvalidShipPlacementException)
    def _place_ships(self, player, board):
        ship_placements = player.get_ship_placements(ships_to_place())

        # Ensure that the ship placements are of the correct format
        try:
            assert len(ship_placements) == len(ships_to_place())
        except AssertionError:
            raise InvalidShipPlacementException

        for ship, location, orientation in ship_placements:
            board.place_ship(ship, location, orientation)

        return board.ship_locations

    @retry(InvalidShotException)
    def _do_shot(self, player, board_to_shoot):
        player_shot = player.get_shot()

        # Ensure that the player is returning a point
        try:
            assert isinstance(player_shot, Point)
        except AssertionError:
            raise NotAPointError

        try:
            is_hit = board_to_shoot.shoot(player_shot)
        except InvalidShotException as e:
            is_hit = e

        return player_shot, is_hit
