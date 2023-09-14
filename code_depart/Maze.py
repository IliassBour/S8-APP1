import pygame
import csv
from Monster import *
from Constants import *
from Door import *


class Maze:
    def __init__(self, mazefile):
        self.tile_size_x = 0
        self.tile_size_y = 0
        self.maze = []
        with open(mazefile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.maze.append(row)
        self.N = len(self.maze)
        self.M = len(self.maze[0])
        self.wallList = []
        self.coinList = []
        self.treasureList = []
        self.obstacleList = []
        self.monsterList = []
        self.doorList = []
        self.exit = []
        self.start = []
        self.tile_size_x = WIDTH/self.M
        self.tile_size_y = HEIGHT / self.N
        self._land_surf = pygame.image.load("assets/Images/land.png")
        self._land_surf = pygame.transform.scale(self._land_surf, (self.tile_size_x, self.tile_size_y))
        self._land_surf_start = pygame.image.load("assets/Images/land_start.png")
        self._land_surf_start = pygame.transform.scale(self._land_surf_start, (self.tile_size_x, self.tile_size_y))
        self._land_surf_finish = pygame.image.load("assets/Images/land_finish.png")
        self._land_surf_finish = pygame.transform.scale(self._land_surf_finish, (self.tile_size_x, self.tile_size_y))
        self._wall_surf = pygame.image.load("assets/Images/wall_9.png")
        self._wall_surf = pygame.transform.scale(self._wall_surf, (self.tile_size_x, self.tile_size_y))
        self._coin_surf = pygame.image.load("assets/Images/coin_1.png")
        self._coin_surf = pygame.transform.scale(self._coin_surf, (ITEM_SIZE*self.tile_size_x, ITEM_SIZE*self.tile_size_y))
        self._treasure_surf = pygame.image.load("assets/Images/treasure_1.png")
        self._treasure_surf = pygame.transform.scale(self._treasure_surf,
                                                 (3*ITEM_SIZE * self.tile_size_x, 2*ITEM_SIZE * self.tile_size_y))
        self._monster_surf = pygame.image.load("assets/Images/golem_3.png")
        self._monster_surf = pygame.transform.scale(self._monster_surf, (self.tile_size_x, self.tile_size_y))
        self._obstacle_surf = pygame.image.load("assets/Images/stones_10.png")
        self._obstacle_surf = pygame.transform.scale(self._obstacle_surf, (ITEM_SIZE*self.tile_size_x, ITEM_SIZE*self.tile_size_y))
        self._door_surf = pygame.image.load("assets/Images/door.png")
        self._door_surf = pygame.transform.scale(self._door_surf, (self.tile_size_x, self.tile_size_y))

    def random_position(self, i, j):
        x = (j + random.uniform(0, 1 - ITEM_SIZE)) * self.tile_size_x
        y = (i + random.uniform(0, 1 - ITEM_SIZE)) * self.tile_size_y
        return x, y

    def make_maze_wall_list(self):
        # Start tile wall
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == '1':
                    cell = pygame.Rect((j * self.tile_size_x, i * self.tile_size_y), (self.tile_size_x, self.tile_size_y))
                    self.wallList.append(cell)
                elif self.maze[i][j] == 'S':
                    # Add conditions for starts not at top.
                    self.start = [(j + 0.2) * self.tile_size_x, (i + 0.2) * self.tile_size_y]
                    cell = pygame.Rect((j * self.tile_size_x, i * self.tile_size_y),
                                       (self.tile_size_x, 0.1 * self.tile_size_y))
                    self.wallList.append(cell)

    def make_maze_item_lists(self):
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == COIN:
                    new_coin = pygame.Rect((self.random_position(i, j)),
                                           (ITEM_SIZE*self.tile_size_x, ITEM_SIZE*self.tile_size_y))
                    self.coinList.append(new_coin)
                elif self.maze[i][j] == TREASURE:
                    new_treasure = pygame.Rect((j * self.tile_size_x, i * self.tile_size_y), (4*ITEM_SIZE*self.tile_size_x, 3*ITEM_SIZE*self.tile_size_y))
                    self.treasureList.append(new_treasure)
                elif self.maze[i][j] == OBSTACLE:
                    new_obstacle = pygame.Rect((self.random_position(i, j)), (ITEM_SIZE*self.tile_size_x, ITEM_SIZE*self.tile_size_y))
                    self.obstacleList.append(new_obstacle)
                elif self.maze[i][j] == MONSTER:
                    new_monster = pygame.Rect((j * self.tile_size_x, i * self.tile_size_y), (self.tile_size_x, self.tile_size_y))
                    self.monsterList.append(Monster(new_monster))
                elif self.maze[i][j] == EXIT:
                    self.exit = pygame.Rect((j * self.tile_size_x, i * self.tile_size_y), (self.tile_size_x, self.tile_size_y))
                elif self.maze[i][j] == DOOR:
                    new_door = pygame.Rect((j * self.tile_size_x, i * self.tile_size_y),
                                              (self.tile_size_x, self.tile_size_y))
                    self.doorList.append(Door(new_door))

    def draw(self, display_surf):
        thinwall_surf = pygame.transform.scale(self._wall_surf, (self.tile_size_x, 0.1 * self.tile_size_y))
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == '1':
                    display_surf.blit(self._wall_surf, (j * self.tile_size_x, i * self.tile_size_y))
                elif self.maze[i][j] == 'S':
                    display_surf.blit(self._land_surf_start, (j * self.tile_size_x, i * self.tile_size_y))
                    display_surf.blit(thinwall_surf, (j * self.tile_size_x, i * self.tile_size_y))
                elif self.maze[i][j] == 'E':
                    display_surf.blit(self._land_surf_finish, (j * self.tile_size_x, i * self.tile_size_y))
                    display_surf.blit(thinwall_surf, (j * self.tile_size_x, (i+0.9) * self.tile_size_y))
                elif self.maze[i][j] == 'D':
                    display_surf.blit(self._door_surf, (j * self.tile_size_x, i * self.tile_size_y))
                else:
                    display_surf.blit(self._land_surf, (j * self.tile_size_x, i * self.tile_size_y))

        for item in self.coinList:
            display_surf.blit(self._coin_surf, item.topleft)

        for item in self.treasureList:
            display_surf.blit(self._treasure_surf, item.topleft)

        for item in self.obstacleList:
            display_surf.blit(self._obstacle_surf, item.topleft)
            #pygame.draw.rect(display_surf, RED, item)

        for item in self.monsterList:
            display_surf.blit(self._monster_surf, item.rect.topleft)

    def make_perception_list(self, player_current, display_surf):
        perception_distance = PERCEPTION_RADIUS * max(self.tile_size_x, self.tile_size_y)
        perception_left = player_current.x + 0.5 * (player_current.size_x - perception_distance)
        perception_top = player_current.y + 0.5 * (player_current.size_y - perception_distance)
        perception_rect = pygame.Rect(perception_left, perception_top, perception_distance, perception_distance)
        wall_list = []
        obstacle_list = []
        item_list = []
        monster_list = []
        door_list = []
        for i in perception_rect.collidelistall(self.wallList):
            wall_list.append(self.wallList[i])
        for i in perception_rect.collidelistall(self.obstacleList):
            obstacle_list.append(self.obstacleList[i])
        for i in perception_rect.collidelistall(self.coinList):
            item_list.append(self.coinList[i])
        for i in perception_rect.collidelistall(self.treasureList):
            item_list.append(self.treasureList[i])
        for i in perception_rect.collidelistall(self.monsterList):
            monster_list.append(self.monsterList[i])
        for i in perception_rect.collidelistall(self.doorList):
            door_list.append(self.doorList[i])

        # POUR DEBUG - tenir la touche "p" pour voir la zone de perception
        # pygame.draw.rect(display_surf, GREEN, perception_rect)
        # pygame.display.flip()
        # print([wall_list, obstacle_list, item_list, monster_list])
        return [wall_list, obstacle_list, item_list, monster_list, door_list]

    def look_at_door(self, player_current, display_surf):
        visible_doors = self.make_perception_list(player_current, display_surf)[4]
        door_state = []
        for door in visible_doors:
            door_state.append(door.check_door())
        return door_state

    def unlock_door(self, key):
        for door in self.doorList:
            if door.unlock_door(key):
                self.doorList.remove(door)