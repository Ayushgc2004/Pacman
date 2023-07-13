import copy
from boards import boards
import pygame
import math
import drawstart

pygame.init()
WIDTH = 900
HEIGHT = 950
blue_pellets = 124
red_pellets = 125
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font("freesansbold.ttf", 20)
level = copy.deepcopy(boards)
color = "blue"
PI = math.pi
player_images = []
new_images = []
for i in range(1, 5):
    player_images.append(
        pygame.transform.scale(
            pygame.image.load(f"assets/player_images/{i}.png"), (45, 45)
        )
    )
for i in range(1, 5):
    new_images.append(
        pygame.transform.scale(
            pygame.image.load(f"assets/new_images/{i}.png"), (45, 45)
        )
    )
blinky_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/red.png"), (45, 45)
)
pinky_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/pink.png"), (45, 45)
)
inky_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/blue.png"), (45, 45)
)
clyde_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/orange.png"), (45, 45)
)
spooked_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/powerup.png"), (45, 45)
)
dead_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/dead.png"), (45, 45)
)
player_x = 800
player_y = 663
player_x1 = 50
player_y1 = 663
direction = 0
blinky_x = 440
blinky_y = 338
blinky_direction = 0
inky_x = 440
inky_y = 388
inky_direction = 2
pinky_x = 440
pinky_y = 438
pinky_direction = 2
clyde_x = 440
clyde_y = 338
clyde_direction = 2
counter = 0
flicker = False
# R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0
direction_command2 = 0
player_speed = 2
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
targets = [
    (player_x, player_y),
    (player_x, player_y),
    (player_x, player_y),
    (player_x, player_y),
]
blinky_dead = False
inky_dead = False
clyde_dead = False
pinky_dead = False
blinky_box = False
inky_box = False
clyde_box = False
pinky_box = False
moving = False
ghost_speeds = [2, 2, 2, 2]
startup_counter = 0
lives = 3
game_over = False
game_won = False
color2 = "red"
direction2 = 1
score2 = 0
startup_counter = 0
lives2 = 3


class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord

        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        if id == 0:
            self.turns, self.in_box = self.check_collisions()
        if id == 1:
            self.turns, self.in_box = self.check_collisions3()
        self.rect = self.draw()

    def move(self, target_x, target_y):
        # Perform A* algorithm to find the path to the target
        path = a_star(
            boards,
            (self.x_pos // 30, self.y_pos // 32),
            (target_x // 30, target_y // 32),
        )
        if path is not None and len(path) > 1:
            next_x, next_y = path[1]
            if next_x > self.x_pos // 30:
                self.direction = 0  # Move right
            elif next_x < self.x_pos // 30:
                self.direction = 1  # Move left
            elif next_y > self.y_pos // 32:
                self.direction = 3  # Move down
            elif next_y < self.y_pos // 32:
                self.direction = 2  # Move up

        # Update the ghost's position based on the current direction
        if self.direction == 0:
            self.x_pos += 1
        elif self.direction == 1:
            self.x_pos -= 1
        elif self.direction == 2:
            self.y_pos -= 1
        elif self.direction == 3:
            self.y_pos += 1
        next_x = self.x_pos
        next_y = self.y_pos

        num1 = (HEIGHT - 50) // 32
        num2 = WIDTH // 30

    def move_blinky(self):
        # r, l, u, d
        # blinky is going to turn whenever colliding with walls, otherwise continue straight
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_clyde(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def draw(self):
        if (not powerup and not self.dead) or (
            eaten_ghost[self.id] and powerup and not self.dead
        ):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect(
            (self.center_x - 18, self.center_y - 18), (36, 36)
        )
        return ghost_rect

    def check_collisions(self):
        # R, L, U, D
        num1 = (HEIGHT - 50) // 32
        num2 = WIDTH // 30
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 or (
                level[self.center_y // num1][(self.center_x - num3) // num2] == 9
                and (self.in_box or self.dead)
            ):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 or (
                level[self.center_y // num1][(self.center_x + num3) // num2] == 9
                and (self.in_box or self.dead)
            ):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 or (
                level[(self.center_y + num3) // num1][self.center_x // num2] == 9
                and (self.in_box or self.dead)
            ):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 or (
                level[(self.center_y - num3) // num1][self.center_x // num2] == 9
                and (self.in_box or self.dead)
            ):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][
                        self.center_x // num2
                    ] < 3 or (
                        level[(self.center_y + num3) // num1][self.center_x // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][
                        self.center_x // num2
                    ] < 3 or (
                        level[(self.center_y - num3) // num1][self.center_x // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][
                        (self.center_x - num2) // num2
                    ] < 3 or (
                        level[self.center_y // num1][(self.center_x - num2) // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[1] = True
                    if level[self.center_y // num1][
                        (self.center_x + num2) // num2
                    ] < 3 or (
                        level[self.center_y // num1][(self.center_x + num2) // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][
                        self.center_x // num2
                    ] < 3 or (
                        level[(self.center_y + num3) // num1][self.center_x // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][
                        self.center_x // num2
                    ] < 3 or (
                        level[(self.center_y - num3) // num1][self.center_x // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][
                        (self.center_x - num3) // num2
                    ] < 3 or (
                        level[self.center_y // num1][(self.center_x - num3) // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[1] = True
                    if level[self.center_y // num1][
                        (self.center_x + num3) // num2
                    ] < 3 or (
                        level[self.center_y // num1][(self.center_x + num3) // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        if self.turns[0] == True:
            if self.center_x > 450:
                self.turns[1] = True
                self.turns[0] = False
        return self.turns, self.in_box

    def check_collisions3(self):
        num1 = (HEIGHT - 50) // 32
        num2 = WIDTH // 30
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 or (
                level[self.center_y // num1][(self.center_x - num3) // num2] == 9
                and (self.in_box or self.dead)
            ):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 or (
                level[self.center_y // num1][(self.center_x + num3) // num2] == 9
                and (self.in_box or self.dead)
            ):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 or (
                level[(self.center_y + num3) // num1][self.center_x // num2] == 9
                and (self.in_box or self.dead)
            ):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 or (
                level[(self.center_y - num3) // num1][self.center_x // num2] == 9
                and (self.in_box or self.dead)
            ):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][
                        self.center_x // num2
                    ] < 3 or (
                        level[(self.center_y + num3) // num1][self.center_x // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][
                        self.center_x // num2
                    ] < 3 or (
                        level[(self.center_y - num3) // num1][self.center_x // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][
                        (self.center_x - num2) // num2
                    ] < 3 or (
                        level[self.center_y // num1][(self.center_x - num2) // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[1] = True
                    if level[self.center_y // num1][
                        (self.center_x + num2) // num2
                    ] < 3 or (
                        level[self.center_y // num1][(self.center_x + num2) // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][
                        self.center_x // num2
                    ] < 3 or (
                        level[(self.center_y + num3) // num1][self.center_x // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][
                        self.center_x // num2
                    ] < 3 or (
                        level[(self.center_y - num3) // num1][self.center_x // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][
                        (self.center_x - num3) // num2
                    ] < 3 or (
                        level[self.center_y // num1][(self.center_x - num3) // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[1] = True
                    if level[self.center_y // num1][
                        (self.center_x + num3) // num2
                    ] < 3 or (
                        level[self.center_y // num1][(self.center_x + num3) // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        if self.turns[1] == True:
            if self.center_x < 450:
                self.turns[0] = True
                self.turns[1] = False

        return self.turns, self.in_box


def a_star(matrix, start, goal):
    # Function to compute the heuristic value (Manhattan distance) between two points
    def heuristic(node, target):
        return abs(node[0] - target[0]) + abs(node[1] - target[1])

    # Function to find the node with the minimum f value in the open set
    def find_min_f(open_set, f_score):
        min_f = float("inf")
        min_node = None
        for node in open_set:
            if f_score[node] < min_f:
                min_f = f_score[node]
                min_node = node
        return min_node

    # Check if the given node is a valid neighbor
    def is_valid_neighbor(node, matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        x, y = node
        if 0 <= x < rows and 0 <= y < cols and matrix[x][y] < 3:
            return True
        return False

    rows = len(matrix)
    cols = len(matrix[0])
    start_node = start
    goal_node = goal
    open_set = [start_node]
    closed_set = []
    g_score = {start_node: 0}
    f_score = {start_node: heuristic(start_node, goal_node)}
    came_from = {}

    while len(open_set) > 0:
        current_node = find_min_f(open_set, f_score)
        if current_node == goal_node:
            path = [current_node]
            while current_node in came_from:
                current_node = came_from[current_node]
                path.append(current_node)
            path.reverse()
            return path

        open_set.remove(current_node)
        closed_set.append(current_node)

        x, y = current_node
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

        for neighbor in neighbors:
            if not is_valid_neighbor(neighbor, matrix) or neighbor in closed_set:
                continue

            tentative_g_score = g_score[current_node] + 1

            if neighbor not in open_set:
                open_set.append(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current_node
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal_node)

    return None


def draw_board():
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(
                    screen,
                    "white",
                    (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)),
                    2,
                )
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(
                    screen,
                    "white",
                    (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)),
                    6,
                )
            if level[i][j] == 3 and j >= 15:
                pygame.draw.line(
                    screen,
                    "blue",
                    (j * num2 + (0.5 * num2), i * num1),
                    (j * num2 + (0.5 * num2), i * num1 + num1),
                    3,
                )
            if level[i][j] == 4 and j >= 15:
                pygame.draw.line(
                    screen,
                    "blue",
                    (j * num2, i * num1 + (0.5 * num1)),
                    (j * num2 + num2, i * num1 + (0.5 * num1)),
                    3,
                )
            if level[i][j] == 9:
                pygame.draw.line(
                    screen,
                    "white",
                    (j * num2, i * num1 + (0.5 * num1)),
                    (j * num2 + num2, i * num1 + (0.5 * num1)),
                    3,
                )
            if level[i][j] == 5 and j >= 15:
                pygame.draw.arc(
                    screen,
                    color,
                    [
                        (j * num2 - (num2 * 0.4)) - 2,
                        (i * num1 + (0.5 * num1)),
                        num2,
                        num1,
                    ],
                    0,
                    PI / 2,
                    3,
                )
            if level[i][j] == 6 and j >= 15:
                pygame.draw.arc(
                    screen,
                    color,
                    [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1],
                    PI / 2,
                    PI,
                    3,
                )
            if level[i][j] == 7 and j >= 15:
                pygame.draw.arc(
                    screen,
                    color,
                    [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1],
                    PI,
                    3 * PI / 2,
                    3,
                )
            if level[i][j] == 8 and j >= 15:
                pygame.draw.arc(
                    screen,
                    color,
                    [
                        (j * num2 - (num2 * 0.4)) - 2,
                        (i * num1 - (0.4 * num1)),
                        num2,
                        num1,
                    ],
                    3 * PI / 2,
                    2 * PI,
                    3,
                )
            if level[i][j] == 3 and j < 15:
                pygame.draw.line(
                    screen,
                    color2,
                    (j * num2 + (0.5 * num2), i * num1),
                    (j * num2 + (0.5 * num2), i * num1 + num1),
                    3,
                )
            if level[i][j] == 4 and j < 15:
                pygame.draw.line(
                    screen,
                    color2,
                    (j * num2, i * num1 + (0.5 * num1)),
                    (j * num2 + num2, i * num1 + (0.5 * num1)),
                    3,
                )
            if level[i][j] == 5 and j < 15:
                pygame.draw.arc(
                    screen,
                    color2,
                    [
                        (j * num2 - (num2 * 0.4)) - 2,
                        (i * num1 + (0.5 * num1)),
                        num2,
                        num1,
                    ],
                    0,
                    PI / 2,
                    3,
                )
            if level[i][j] == 6 and j < 15:
                pygame.draw.arc(
                    screen,
                    color2,
                    [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1],
                    PI / 2,
                    PI,
                    3,
                )
            if level[i][j] == 7 and j < 15:
                pygame.draw.arc(
                    screen,
                    color2,
                    [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1],
                    PI,
                    3 * PI / 2,
                    3,
                )
            if level[i][j] == 8 and j < 15:
                pygame.draw.arc(
                    screen,
                    color2,
                    [
                        (j * num2 - (num2 * 0.4)) - 2,
                        (i * num1 - (0.4 * num1)),
                        num2,
                        num1,
                    ],
                    3 * PI / 2,
                    2 * PI,
                    3,
                )


def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(
            pygame.transform.flip(player_images[counter // 5], True, False),
            (player_x, player_y),
        )
    elif direction == 2:
        screen.blit(
            pygame.transform.rotate(player_images[counter // 5], 90),
            (player_x, player_y),
        )
    elif direction == 3:
        screen.blit(
            pygame.transform.rotate(player_images[counter // 5], 270),
            (player_x, player_y),
        )


def draw_player2():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(inky_img, (player_x, player_y))
    elif direction == 1:
        screen.blit(
            pygame.transform.flip(inky_img, True, False),
            (player_x, player_y),
        )
    elif direction == 2:
        screen.blit(inky_img, (player_x, player_y))
    elif direction == 3:
        screen.blit(inky_img, (player_x, player_y))


def draw_player3():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction2 == 0:
        screen.blit(new_images[counter // 5], (player_x1, player_y1))
    elif direction2 == 1:
        screen.blit(
            pygame.transform.flip(new_images[counter // 5], True, False),
            (player_x1, player_y1),
        )
    elif direction2 == 2:
        screen.blit(
            pygame.transform.rotate(new_images[counter // 5], 90),
            (player_x1, player_y1),
        )
    elif direction2 == 3:
        screen.blit(
            pygame.transform.rotate(new_images[counter // 5], 270),
            (player_x1, player_y1),
        )


def draw_player4():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction2 == 0:
        screen.blit(pinky_img, (player_x1, player_y1))
    elif direction2 == 1:
        screen.blit(
            pygame.transform.flip(pinky_img, True, False),
            (player_x1, player_y1),
        )
    elif direction2 == 2:
        screen.blit(pinky_img, (player_x1, player_y1))
    elif direction2 == 3:
        screen.blit(pinky_img, (player_x1, player_y1))


def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


def check_position2(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction2 == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction2 == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction2 == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction2 == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction2 == 2 or direction2 == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction2 == 0 or direction2 == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


def check_collisions(scor):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50

    return scor


def check_collisions2(scor):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y1 // num1][center_x1 // num2] == 1:
            level[center_y1 // num1][center_x1 // num2] = 0
            scor += 10
        if level[center_y1 // num1][center_x1 // num2] == 2:
            level[center_y1 // num1][center_x1 // num2] = 0
            scor += 50
    return scor


def move_player(play_x, play_y):
    # r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y


def move_player2(play_x, play_y):
    # r, l, u, d
    if direction2 == 0 and turns_allowed2[0]:
        play_x += player_speed
    elif direction2 == 1 and turns_allowed2[1]:
        play_x -= player_speed
    if direction2 == 2 and turns_allowed2[2]:
        play_y -= player_speed
    elif direction2 == 3 and turns_allowed2[3]:
        play_y += player_speed
    return play_x, play_y


run = True
while run:
    print(score, score2)
    if lives == 0:
        print("player1 has won")
        print("final score2:", score2)
        break
    if lives2 == 0:
        print("player2 has won")
        print("final score: ", score)
        break
    if score == red_pellets * 10:
        print("Blue side has won the game")
        print("final score: ", score)
        break
    if score2 == blue_pellets * 10:
        print("red side has won the game")
        print("score : ", score2)
        break
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill("black")
    draw_board()
    center_x = player_x + 23
    center_y = player_y + 24
    center_x1 = player_x1 + 23
    center_y1 = player_y1 + 24
    if player_x < 450:
        draw_player()
    else:
        draw_player2()
    if player_x1 < 450:
        draw_player4()
    else:
        draw_player3()
    # draw_player3()

    blinky = Ghost(
        blinky_x,
        blinky_y,
        targets[0],
        ghost_speeds[0],
        blinky_img,
        blinky_direction,
        blinky_dead,
        blinky_box,
        0,
    )
    clyde = Ghost(
        clyde_x,
        clyde_y,
        targets[0],
        ghost_speeds[0],
        clyde_img,
        clyde_direction,
        clyde_dead,
        clyde_box,
        1,
    )
    player_circle = pygame.draw.circle(screen, "#00FFFF", (center_x, center_y), 20, 2)
    player_circle1 = pygame.draw.circle(
        screen, "#00FFFF", (center_x1, center_y1), 20, 2
    )

    turns_allowed = check_position(center_x, center_y)
    turns_allowed2 = check_position2(center_x1, center_y1)
    if moving == True:
        player_x, player_y = move_player(player_x, player_y)
        player_x1, player_y1 = move_player2(player_x1, player_y1)
        blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
    if player_x < 450:
        score = check_collisions(score)
    if player_x1 > 450:
        score2 = check_collisions2(score2)
    # blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
    # clyde_x,clyde_y,clyde_direction = clyde.move_clyde()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and direction_command == 0:
                    direction_command = direction
                if event.key == pygame.K_LEFT and direction_command == 1:
                    direction_command = direction
                if event.key == pygame.K_UP and direction_command == 2:
                    direction_command = direction
                if event.key == pygame.K_DOWN and direction_command == 3:
                    direction_command = direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                direction_command2 = 0
            if event.key == pygame.K_a:
                direction_command2 = 1
            if event.key == pygame.K_w:
                direction_command2 = 2
            if event.key == pygame.K_s:
                direction_command2 = 3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d and direction_command2 == 0:
                    direction_command2 = direction
                if event.key == pygame.K_a and direction_command2 == 1:
                    direction_command2 = direction
                if event.key == pygame.K_w and direction_command2 == 2:
                    direction_command2 = direction
                if event.key == pygame.K_w and direction_command2 == 3:
                    direction_command2 = direction

    if player_circle.colliderect(blinky.rect) and not blinky.dead:
        if lives > 0:
            startup_counter == 0
            player_x = 800
            player_y = 663

            direction = 0
            blinky_x = 440
            blinky_y = 388
            blinky_direction = 0

            direction_command = 0
            lives -= 1

    if player_circle1.colliderect(clyde.rect) and not clyde.dead:
        if lives2 > 0:
            startup_counter == 0
            player_x1 = 50
            player_y1 = 663

            direction2 = 2
            clyde_x = 440
            clyde_y = 338

            clyde_direction = 0

            direction_command2 = 0
            lives2 -= 1

    if direction_command2 == 0 and turns_allowed2[0]:
        direction2 = 0
    if direction_command2 == 1 and turns_allowed2[1]:
        direction2 = 1
    if direction_command2 == 2 and turns_allowed2[2]:
        direction2 = 2
    if direction_command2 == 3 and turns_allowed2[3]:
        direction2 = 3

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    pygame.display.flip()
pygame.quit()
