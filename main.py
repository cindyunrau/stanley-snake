import random
import typing
import collections
from collections import Counter

MOVES_MATH = {"up": [0,1], "down": [0,-1], "left": [-1,0], "right": [1,0]}
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
MOVES = ["up","down","left","right"]
# GAME_ID = None
# BOARD = None
# BOUNDS = None

# IDEAS:
#   - recursive, where # levels = space lookahead

# TO-DO:
#   - alter for multiple gamemodes (low)
#   - 

def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "cindyunrau",
        "color": "#aeeb34",
        "head": "snail",
        "tail": "comet",
    }

def start(game_state: typing.Dict):
    print("GAME ON!!!")

    GAME_ID = game_state["game"]["id"]
    BOARD = {"width": game_state["board"]["width"],"height":game_state["board"]["height"]}
    BOUNDS = {"min_x":0,"max_x":BOARD["width"]-1,"min_y":0,"max_y":BOARD["height"]-1}

    print("\tGame ID:",GAME_ID)
    print("\tBoard Dimensions:",str(BOARD))
    print("\tBoundaries:",str(BOUNDS))

def end(game_state: typing.Dict):
    print("gg")
    print("WHAT'S DONE IS DONE\n")

def get_reachable(center):
    return {"up":{"x":center["x"],"y":center["y"]+1},"down":{"x":center["x"],"y":center["y"]-1},"left":{"x":center["x"]-1,"y":center["y"]},"right":{"x":center["x"]+1,"y":center["y"]}}

def get_safe(my_body,my_length,snakes):
    my_head = my_body[0]
    possible_moves = get_reachable(my_head)
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # avoid walls
    if my_head["x"] == BOUNDS["x_min"]:
        print("WALL: NO LEFT", my_head["x"])
        is_move_safe["left"] = False
    elif my_head["x"] == BOUNDS["x_max"]:
        print("WALL: NO RIGHT", my_head["x"])
        is_move_safe["right"] = False
    if my_head["y"] == BOUNDS["y_min"]:
        print("WALL: NO DOWN", my_head["y"])
        is_move_safe["down"] = False
    elif my_head["y"] == BOUNDS["x_max"]:
        print("WALL: NO UP", my_head["y"])
        is_move_safe["up"] = False

    # avoid body
    for move, isSafe in is_move_safe.items():
        if isSafe:
            if possible_moves[move] in my_body:
                print("BODY: NO", move.upper(), possible_moves[move], my_body)
                is_move_safe[move] = False

    # avoid snakes (NOT TESTED)
    for move, isSafe in is_move_safe.items():
        if isSafe:
            for snake in snakes:
                    if possible_moves[move] in snake["body"]:
                        print("SNAKE: NO", move.upper(), possible_moves[move], snake["body"])
                        is_move_safe[move] = False
    
    # tail is safe
    if(my_length>2):
        for move, coords in possible_moves.items():
            if coords == my_body[-1]:
                is_move_safe[move] = True

    return is_move_safe

def board_to_arr():
    arr = []
    for i in BOARD["width"]:
        arr.append([])
        for j in BOARD["height"]:
                arr[i].append("-1")

    return arr


def move(game_state: typing.Dict) -> typing.Dict:
    GAME_ID = game_state["game"]["id"]
    BOARD = {"width": game_state["board"]["width"],"height":game_state["board"]["height"]}
    global BOUNDS
    BOUNDS = {"x_min":0,"x_max":BOARD["width"]-1,"y_min":0,"y_max":BOARD["height"]-1}

    my_body = game_state["you"]["body"]
    
    my_length = game_state["you"]["length"]
    my_health = game_state["you"]["health"]

    food = game_state["board"]["food"]
    hazards = game_state["board"]["hazards"]

    garbage_snakes = game_state["board"]["snakes"]

    moves = {"up": [0,1], "down": [0,-1], "left": [-1,0], "right": [1,0]}

    is_move_safe = get_safe(my_body,my_length,garbage_snakes)
    print(is_move_safe)

    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # TO-DOs:

    # Prioritize food when: 
    #   - Health Low (2)
    if(my_health<25): # Determine optimal threshold
        pass

    #   - Food close by

    #   - Other snakes "much" larger / I am small

    # Given a movement choice, pick the one with the longest possible path (1)
    #   - take moving snakes into account

    # Better idling strategy?
    next_move = random.choice(safe_moves)

    # Snake personality possibilities
    #   - aggressive
    #       - attack closest snake that is smaller than me
    #       - pin snake against obstacles (wall, my body, other bodies)
    #   - defensive, get food when needed, otherwise make safe moves

    # Perform pathfinding on other snakes

    # Assign risk values to each coordinate

    # Algorithms
    #   - A* - path search
    #   - Flood fill - find open areas
    #   - Minimax - tree search
    #   - Monte Carlo - tree search
    #   - Voronoi - estimate board area control



    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
