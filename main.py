# 28/02/2021
# Pathfinder
# TODO Create Destination and entry node
# TODO Add diagonal movements
# TODO Force quit / exit search
# TODO Mouse drag

import pygame
import sys
import constants
from functions import *


def main():
    list_of_block_location_lists = draw_grid()
    logic_table = generate_logic_table()
    src_dst_node_state = [False, False]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                position, cell_logic, cell_index = did_player_clicked_on_block(list_of_block_location_lists, logic_table, mouse_x, mouse_y)
                if position != INVALID_BLOCK_SELECTED_FLAG:
                    logic_table, src_dst_node_state = draw_block(position, cell_logic, cell_index, logic_table, src_dst_node_state)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    src_node_state = src_dst_node_state[0]
                    dst_node_state = src_dst_node_state[0]
                    if src_node_state and dst_node_state:
                        path_find(logic_table)


if __name__ == "__main__":
    main()
