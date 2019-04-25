def format_ship_placement(placements : list):
    return [ {'x': p[0], 'y': p[1], 'state': 's'} for p in placements]

def format_shot_placement(shots : list, placements : list):
    return [ {'x': s[0], 'y': s[1], 'state': 'h' if s in placements else 'm'} for s in shots]

def format_match_output(match_data : list):
    # At the moment, we only deal with 1 game matches
    game = match_data[0]

    new_game = {
            'teams': [game['p1_name'], game['p2_name']],
            'ships': [format_ship_placement(game['p1_ship_placements']), format_ship_placement(game['p2_ship_placements'])],
            'shots': [format_shot_placement(game['p1_shots'], game['p2_ship_placements']), format_shot_placement(game['p2_shots'], game['p1_ship_placements'])],
            'winner': game['winner']
        }

    return {'game': new_game}