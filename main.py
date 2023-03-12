import random
import typing
import collections
from collections import Counter
from pprint import pprint

MOVES_MATH = {"up": [0,1], "down": [0,-1], "left": [-1,0], "right": [1,0]}
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
MOVES = ["up","down","left","right"]

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

def get_all_safe(obstacles):
    safe = []
    for i in range(BOARD["width"]):
        for j in range(BOARD["height"]):
            if obstacles[i][j] == False:
                safe.append([i,j])            

    return safe_moves

def get_safe(point,obstacles):
    possible_moves = get_reachable(point)
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # # avoid walls
    # if my_head["x"] == BOUNDS["x_min"]:
    #     print("WALL: NO LEFT", my_head["x"])
    #     is_move_safe["left"] = False
    # elif my_head["x"] == BOUNDS["x_max"]:
    #     print("WALL: NO RIGHT", my_head["x"])
    #     is_move_safe["right"] = False
    # if my_head["y"] == BOUNDS["y_min"]:
    #     print("WALL: NO DOWN", my_head["y"])
    #     is_move_safe["down"] = False
    # elif my_head["y"] == BOUNDS["x_max"]:
    #     print("WALL: NO UP", my_head["y"])
    #     is_move_safe["up"] = False


    for move, isSafe in is_move_safe.items():
        if isSafe:
            if possible_moves[move] in obstacles:
                print("OBSTACLE: NO", move.upper(), possible_moves[move])
                is_move_safe[move] = False

    # # avoid snakes (NOT TESTED)
    # for move, isSafe in is_move_safe.items():
    #     if isSafe:
    #         for snake in snakes:
    #                 if possible_moves[move] in snake["body"]:
    #                     print("SNAKE: NO", move.upper(), possible_moves[move], snake["body"])
    #                     is_move_safe[move] = False
    


    return is_move_safe

def board_to_arr(width,height,init):
    arr = []
    for i in range(width):
        arr.append([])
        for j in range(height):
                arr[i].append(init)

    return arr


# if space is empty, call flood fill on it
# if no neighbors are empty, return
# assumes init position is safe
def flood_fill_init(init_x,init_y,obstacles):
    start = [init_x,init_y] #[init_x,init_y] # {"x":init_x,"y":init_y,"visited":False}
    board = board_to_arr(BOARD["width"],BOARD["height"],-1)
    queue = []
    queue.append(start)
    board[init_x][init_y] = 0

    x = flood_fill(queue,board,obstacles,0)
    return x

def get_adjacent(center):
    return [[center[0]+1,center[1]],[center[0]-1,center[1]],[center[0],center[1]+1],[center[0],center[1]-1]]

def is_in_bound(point):
    if point[0]>=BOUNDS["x_min"] and point[0]<=BOUNDS["x_max"]:
        if point[1]>=BOUNDS["y_min"] and point[1]<=BOUNDS["y_max"]:
            return True
    return False

def flood_fill(queue,board,obstacles,size):
    if len(queue) == 0:
        return size
    
    size = size + 1

    start = queue.pop(0)
    adjacent = get_adjacent(start)
    
    for square in adjacent:
        if is_in_bound(square) and obstacles[square[0]][square[1]] == False:
            if board[square[0]][square[1]] == -1:
                queue.append(square)
                board[square[0]][square[1]] = board[start[0]][start[1]] + 1

    return flood_fill(queue,board,obstacles,size)


def move(game_state: typing.Dict) -> typing.Dict:
    GAME_ID = game_state["game"]["id"]
    # To-do: remove global var
    global BOARD
    BOARD = {"width": game_state["board"]["width"],"height":game_state["board"]["height"]}
    global BOUNDS
    BOUNDS = {"x_min":0,"x_max":BOARD["width"]-1,"y_min":0,"y_max":BOARD["height"]-1}

    walls = []
    for i in range(BOARD["width"]):
        walls.append({"x":i,"y":-1})
        walls.append({"x":i,"y":BOARD["height"]})
    for i in range(BOARD["height"]):
        walls.append({"x":-1,"y":i})
        walls.append({"x":BOARD["width"],"y":i})

    my_head = game_state["you"]["body"][0]
    my_body = game_state["you"]["body"][1:]
    
    my_length = game_state["you"]["length"]
    my_health = game_state["you"]["health"]

    food = game_state["board"]["food"]
    hazards = game_state["board"]["hazards"]

    garbage_snakes = game_state["board"]["snakes"]

    moves_coord = {"up": [0,1], "down": [0,-1], "left": [-1,0], "right": [1,0]}

    obstacles = board_to_arr(BOARD["width"],BOARD["height"],False)
    obstacles_dict = []

    obstacles[my_head["x"]][my_head["y"]] = True
    obstacles_dict.append(my_head)

    obstacles_dict.extend(my_body)

    for body_elem in my_body:
        obstacles[body_elem["x"]][body_elem["y"]] = True
        # obstacles_dict.extend(body_elem)


    for snake in garbage_snakes:
        for body_elem in snake["body"]:
            obstacles[body_elem["x"]][body_elem["y"]] = True
            # obstacles_dict.extend(body_elem)
        obstacles_dict.extend(snake["body"])

    obstacles_dict.extend(walls)

    # for wall_elem in walls:
    #     # obstacles[wall_elem["x"]][wall_elem["y"]] = True
    #     obstacles_dict.append(wall_elem)

    # print("ObstaclesD:",obstacles_dict)
    # print("Obstacles:",obstacles)
    
    is_move_safe = get_safe(my_head,obstacles_dict)

    path_lengths = {"up": 0, "down": 0, "left": 0, "right": 0}
    for move, isSafe in is_move_safe.items():
        if isSafe:
            path_lengths[move] = flood_fill_init(my_head["x"]+moves_coord[move][0],my_head["y"]+moves_coord[move][1],obstacles)

    print("PATH LEN:",path_lengths)


    
    # # tail is safe
    # if(my_length>2):
    #     for move, coords in possible_moves.items():
    #         if coords == my_body[-1]:
    #             is_move_safe[move] = True

    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    print("SAFE:",safe_moves)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}


    # safe = get_all_safe(obstacles)

    

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
    longest_path = 0
    for move, path_len in path_lengths.items():
        if path_len > longest_path:
            longest_path = path_len
    
    moves = []
    for move, path_len in path_lengths.items():
        if path_len == longest_path:
            moves.append(move)
    
    print("LONGEST PATH IS", longest_path, "WITH POSSIBLE DIRECTIONS:", moves)
    next_move = random.choice(moves)

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
