import importlib
import logging
import stopit

from config import MAX_SHOT_TIME, MAX_PLACE_TIME
from exceptions import (
    InvalidShipPlacementException,
    InvalidShotException,
    MaxRetriesExceededException,
    NotAPointError,
)
from game_types.Board import Board
from game_types.Point import Point
from game_types.Ship import ships_to_place
from utils import retry

logging.basicConfig(filename='games.log', level=logging.DEBUG)


# TODO: Test game - all cases


class Game:
    def __init__(self, players, game_id):

        # Set game_id
        self.game_id = game_id

        # Create boards
        self.first_player_board = Board()
        self.second_player_board = Board()

        # Import the players
        bots_path = "bots"
        self.player_bots = [
            getattr(importlib.import_module(f"{bots_path}.{p}"), p)() for p in players
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

        logging.info(f'------------ Starting game {self.game_id} between {self.first_player.name} and {self.second_player.name} ------------')

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
                p1_shot, p1_is_hit, p1_is_sunk, p1_ship_sunk, error = self._do_shot(self.first_player, self.second_player_board)
                p1_shots.append(p1_shot)
                logging.info(f'{self.first_player.name} shot at {p1_shot} and {"hit" if p1_is_hit else "missed"}')

                if p1_is_sunk:
                    logging.info(f'{self.first_player.name} sunk {self.second_player.name}\'s {p1_ship_sunk}!')

                self.first_player.last_shot_status = {'shot': p1_shot,
                                                      'is_hit': p1_is_hit,
                                                      'is_sunk': p1_is_sunk,
                                                      'ship_sunk': p1_ship_sunk,
                                                      'error': error}

            except MaxRetriesExceededException:
                self.first_player.last_shot_status = {'shot': None,
                                                      'is_hit': None,
                                                      'is_sunk': None,
                                                      'ship_sunk': None,
                                                      'error': MaxRetriesExceededException}

            if self.second_player_board.is_board_lost():
                winner = self.first_player.name
                break

            # Get second player shot
            try:
                p2_shot, p2_is_hit, p2_is_sunk, p2_ship_sunk, error = self._do_shot(self.second_player, self.first_player_board)
                p2_shots.append(p2_shot)
                logging.info(f'{self.second_player.name} shot at {p2_shot} and {"hit" if p2_is_hit else "missed"}')

                if p2_is_sunk:
                    logging.info(f'{self.second_player.name} sunk {self.first_player.name}\'s {p2_ship_sunk}!')

                self.second_player.last_shot_status = {'shot': p2_shot,
                                                       'is_hit': p2_is_hit,
                                                       'is_sunk': p2_is_sunk,
                                                       'ship_sunk': p2_ship_sunk,
                                                       'error': error}

            except MaxRetriesExceededException:
                self.second_player.last_shot_status = {'shot': None,
                                                       'is_hit': None,
                                                       'is_sunk': None,
                                                       'ship_sunk': None,
                                                       'error': MaxRetriesExceededException}

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

    @retry((InvalidShipPlacementException, stopit.utils.TimeoutException))
    def _place_ships(self, player, board):

        with stopit.ThreadingTimeout(MAX_PLACE_TIME, swallow_exc=False):
            ship_placements = player.get_ship_placements(ships_to_place())

        # Ensure that the ship placements are of the correct format
        try:
            assert isinstance(ship_placements, list)
            assert len(ship_placements) == len(ships_to_place())
        except AssertionError:
            raise InvalidShipPlacementException

        for ship, location, orientation in ship_placements:
            board.place_ship(ship, location, orientation)

        return board.all_ship_locations

    @retry((InvalidShotException, stopit.utils.TimeoutException))
    def _do_shot(self, player, board_to_shoot):

        error = None

        # Call get_shot and enforce the timeout
        with stopit.ThreadingTimeout(MAX_SHOT_TIME, swallow_exc=False):
            player_shot = player.get_shot()

        # If this succeeded, ensure the player is returning a point
        try:
            assert isinstance(player_shot, Point)
        # If not - fail
        except AssertionError:
            is_hit = None
            is_sunk = False
            ship_sunk = None
            error = NotAPointError

            return player_shot, is_hit, is_sunk, ship_sunk, error

        # finally, if everything is ok, try and perform the shot
        try:
            is_hit, is_sunk, ship_sunk = board_to_shoot.shoot(player_shot)
        except InvalidShotException:
            is_hit = None
            is_sunk = False
            ship_sunk = None
            error = InvalidShotException

        return player_shot, is_hit, is_sunk, ship_sunk, error
