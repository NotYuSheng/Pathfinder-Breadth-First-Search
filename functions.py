import pygame
import sys
from constants import *


def generate_logic_table():
    """Create logic table"""

    logic_table = []
    for index in range(NUM_OF_GRID):
        logic_table.append([])
        for __ in range(NUM_OF_GRID):
            logic_table[index].append(EMPTY_FLAG)
    return logic_table


def draw_grid() -> list:
    """Creates grid, retun a list of all block locations"""

    list_of_block_location_lists = []

    for y_index in range(0, NUM_OF_GRID):
        for x_index in range(0, NUM_OF_GRID):
            block_x = TOP_LEFT_BLOCK_X + PIX_GRID_SIZE * x_index
            block_y = TOP_LEFT_BLOCK_Y + PIX_GRID_SIZE * y_index
            position = (block_x, block_y)
            pygame.draw.rect(FRAME, WHITE, (position, WIDTH_HEIGHT))
            top_left_position = list(position)
            bottom_right_position = [top_left_position[0] + WIDTH_HEIGHT[0], top_left_position[1] + WIDTH_HEIGHT[1]]
            list_of_block_location_lists.append([top_left_position, bottom_right_position])

    pygame.display.update()
    return list_of_block_location_lists


def did_player_clicked_on_block(list_of_block_location_lists: list, logic_table: list, mouse_x: int, mouse_y: int):
    """
    Check which block selected
    Return block location and cell logic
    INVALID_BLOCK_SELECTED_FLAG and INVALID_FLAG if no block selected
    """

    block_index_x = 0
    block_index_y = 0

    for block_location_list in list_of_block_location_lists:
        min_block_x = block_location_list[0][0]
        max_block_x = block_location_list[1][0]
        min_block_y = block_location_list[0][1]
        max_block_y = block_location_list[1][1]

        within_range = min_block_x < mouse_x < max_block_x and min_block_y < mouse_y < max_block_y

        if within_range:
            position = (min_block_x, min_block_y)
            cell_logic = logic_table[block_index_y][block_index_x]
            cell_index = [block_index_x, block_index_y]
            return position, cell_logic, cell_index

        block_index_x += 1

        if block_index_x > (NUM_OF_GRID - 1):
            block_index_x = 0
            block_index_y += 1

    return INVALID_BLOCK_SELECTED_FLAG, INVALID_FLAG, INVALID_INDEX


def draw_block(position: list, cell_logic: list, cell_index: list, logic_table: list, src_dst_node_state: list):
    """
    Draw block
    Return logic_table, src_dst_node_state
    """

    src_node_state = src_dst_node_state[0]
    dst_node_state = src_dst_node_state[1]

    if cell_logic == SRC_FLAG:
        # Invert if it is start node
        color = EMPTY_BLOCK_COLOR
        flag = EMPTY_FLAG
        src_node_state = False

    elif cell_logic == DST_FLAG:
        # Invert if it is destination node
        color = EMPTY_BLOCK_COLOR
        flag = EMPTY_FLAG
        dst_node_state = False

    elif cell_logic == WALL_FLAG:
        # Invert if already a wall
        color = EMPTY_BLOCK_COLOR
        flag = EMPTY_FLAG

    elif not src_node_state:
        color = SRC_BLOCK_COLOR
        flag = SRC_FLAG
        src_node_state = True

    elif not dst_node_state:
        color = DST_BLOCK_COLOR
        flag = DST_FLAG
        dst_node_state = True

    else:
        # Create wall
        color = WALL_BLOCK_COLOR
        flag = WALL_FLAG

    logic_table[cell_index[1]][cell_index[0]] = flag

    # Draw Rect
    pygame.draw.rect(FRAME, color, (position, WIDTH_HEIGHT))
    pygame.display.update()

    src_dst_node_state = [src_node_state, dst_node_state]

    return logic_table, src_dst_node_state


def get_flag_loc(logic_table: list, flag: int) -> list:
    """Find and return the flag location"""

    block_index_x = 0
    block_index_y = 0

    for row in logic_table:
        for cell_logic in row:
            if cell_logic == flag:
                position = [block_index_x, block_index_y]
                return position

            block_index_x += 1

            if block_index_x > (NUM_OF_GRID - 1):
                block_index_x = 0
                block_index_y += 1


def try_next_node(current_loc: list, orientation: str, logic_table: list) -> bool:
    """Return if direction is valid"""

    current_loc_x = current_loc[0]
    current_loc_y = current_loc[1]

    if orientation == "L":
        next_loc = [current_loc_x - 1, current_loc_y]
    elif orientation == "R":
        next_loc = [current_loc_x + 1, current_loc_y]
    elif orientation == "U":
        next_loc = [current_loc_x, current_loc_y - 1]
    elif orientation == "D":
        next_loc = [current_loc_x, current_loc_y + 1]

    # Check if out of range
    next_loc_x = next_loc[0]
    next_loc_y = next_loc[1]

    if next_loc_x < 0 or next_loc_y < 0:
        return False

    elif next_loc_x > NUM_OF_GRID - 1 or next_loc_y > NUM_OF_GRID - 1:
        return False

    # Check if next location is wall or src node
    if logic_table[next_loc_y][next_loc_x] == WALL_FLAG or logic_table[next_loc_y][next_loc_x] == SRC_FLAG:
        return False
    return True


def get_first_moves(src_loc: list, logic_table: list) -> list:
    """Get all valid first moves and return elements"""

    list_of_elements = []

    if try_next_node(src_loc, "L", logic_table):
        list_of_elements.append("L")

    if try_next_node(src_loc, "R", logic_table):
        list_of_elements.append("R")

    if try_next_node(src_loc, "U", logic_table):
        list_of_elements.append("U")

    if try_next_node(src_loc, "D", logic_table):
        list_of_elements.append("D")

    return list_of_elements


def get_location(src_loc: list, route: str) -> list:
    """Move from source location based on route, return end location"""

    current_location = src_loc[:]
    for char in route:
        if char == "L":
            current_location[0] -= 1
            continue
        elif char == "R":
            current_location[0] += 1
            continue
        elif char == "U":
            current_location[1] -= 1
            continue
        elif char == "D":
            current_location[1] += 1
            continue
    return current_location


def draw_path(src_loc: list, route: str, route_color: str):
    """Draw path onto frame"""

    for index in range(1, len(route)):
        current_route = route[:index]
        current_location = get_location(src_loc, current_route)

        x_location = current_location[0]
        y_location = current_location[1]

        position_x = TOP_LEFT_BLOCK_X + PIX_GRID_SIZE * x_location
        position_y = TOP_LEFT_BLOCK_Y + PIX_GRID_SIZE * y_location
        position = (position_x, position_y)

        pygame.draw.rect(FRAME, route_color, (position, WIDTH_HEIGHT))

    pygame.display.update()


def queue_element_can_be_expanded(current_location: list, logic_table: list) -> bool:
    """Check if this route can further expanded or is at dead end"""

    if try_next_node(current_location, "L", logic_table):
        return True
    elif try_next_node(current_location, "R", logic_table):
        return True
    elif try_next_node(current_location, "U", logic_table):
        return True
    return try_next_node(current_location, "D", logic_table)


def get_new_elements(current_location: list, queue_element: str, logic_table: list):
    """Return a list of new queue elements"""

    new_queue_elements = []
    previous_move = queue_element[-1]

    if try_next_node(current_location, "L", logic_table) and previous_move != "R":
        new_queue_elements.append(queue_element + "L")

    if try_next_node(current_location, "R", logic_table) and previous_move != "L":
        new_queue_elements.append(queue_element + "R")

    if try_next_node(current_location, "U", logic_table) and previous_move != "D":
        new_queue_elements.append(queue_element + "U")

    if try_next_node(current_location, "D", logic_table) and previous_move != "U":
        new_queue_elements.append(queue_element + "D")

    return new_queue_elements


def find_successful_route(logic_table: list, queue: list, src_loc: list, dst_loc: list) -> str:
    """
    Return the first route able to reach the destination node
    Return NO_VALID_ROUTE_FLAG if unable to reach destination node
    """

    while len(queue) > 0:
        queue_element = queue[0]

        draw_path(src_loc, queue_element, SEARCH_BLOCK_COLOR)
        current_location = get_location(src_loc, queue_element)

        # Check if queue element at dead end
        if not queue_element_can_be_expanded(current_location, logic_table):
            draw_path(src_loc, queue_element, EMPTY_BLOCK_COLOR)
            queue.remove(queue_element)
            continue

        # Expand queue element
        new_queue_elements = get_new_elements(current_location, queue_element, logic_table)

        # Check if any of the new elements are at destination
        for new_queue_element in new_queue_elements:
            current_location = get_location(src_loc, new_queue_element)
            if current_location == dst_loc:
                draw_path(src_loc, queue_element, EMPTY_BLOCK_COLOR)
                return new_queue_element

            queue.append(new_queue_element)

        draw_path(src_loc, queue_element, EMPTY_BLOCK_COLOR)

        queue.remove(queue_element)

    return NO_VALID_ROUTE_FLAG


def path_find(logic_table: list):
    """Path find main"""

    src_loc = get_flag_loc(logic_table, SRC_FLAG)
    dst_loc = get_flag_loc(logic_table, DST_FLAG)

    queue = get_first_moves(src_loc, logic_table)

    successful_route = find_successful_route(logic_table, queue, src_loc, dst_loc)

    if successful_route == NO_VALID_ROUTE_FLAG:
        print("Unable reach destination")
    else:
        print(successful_route)
        draw_path(src_loc, successful_route, SUCCESSFUL_ROUTE_COLOR)
