import numpy as np

class A_star:
    def __init__(self, pos, goal):
        self.path = {}
        self.current_pos = pos
        self.goal = goal
        self.index = 0
        self.cost = 0
        self.predecessor = -1

    def calculate_heuristic(self, pos):
        return np.sqrt(np.power(pos[0]-self.goal[0], 2) + np.power(pos[1]-self.goal[1], 2))

    def possible_path(self, around, pos):
        wall_up, wall_down, wall_left, wall_right = False, False, False, False

        for wall in around:
            if wall[0] + wall[2] < pos[0]: #Mur à gauche
                wall_left = True
            elif wall[0] > pos[0]: #Mur à droite
                wall_right = True
            elif wall[1] + wall[3] < pos[1]: #Mur en haut
                wall_up = True
            elif wall[1] > pos[1]: #Mur en bas
                wall_down = True
        return wall_up, wall_down, wall_left, wall_right

    def next_move(self, wall_up, wall_down, wall_left, wall_right, heuristic):


        if self.index == 0:
            self.path[str(self.index)] = [self.predecessor, self.cost+heuristic, wall_up, wall_down, wall_left, wall_right] #parent
            self.predecessor = self.index
            self.index += 1
            self.cost += 1
        else:
            self.path[str(self.index)] = [self.predecessor, self.cost + heuristic, wall_up, wall_down, wall_left, wall_right]
            self.predecessor = self.index
            self.index += 1
            self.cost += 1

        if wall_down == False:
            return "DOWN"
        elif wall_right == False:
            return "RIGHT"
        elif wall_left == False:
            return "LEFT"
        elif wall_right == False:
            return "UP"

        return "ERROR"