from logic.utils import Direction, GHOST_COLORS
import pygame
import random


class MovableObject:
    def __init__(self, game_controller, x, y, size: int, speed, color=(255, 0, 0)):
        self.current_direction = Direction.NONE
        self.previous_direction = Direction.NONE

        self.size = size
        self.controller = game_controller
        self.surface = game_controller.game_screen
        self.color = color
        self.y = y
        self.x = x
        self.image = None
        self.speed = speed

    def collides_with_wall(self, in_position):
        collision_rect = pygame.Rect(in_position[0], in_position[1], self.size, self.size)
        collides = False
        walls = self.controller.walls
        for wall in walls:
            collides = collision_rect.colliderect(wall.get_shape())
            if collides: break
        return collides

    def calculate_position(self, in_direction: Direction):
        desired_position = (self.x, self.y)
        if in_direction == Direction.NONE:
            return desired_position
        elif in_direction == Direction.UP:
            return (self.x, self.y - self.speed)
        elif in_direction == Direction.DOWN:
            return (self.x, self.y + self.speed)
        elif in_direction == Direction.LEFT:
            return (self.x - self.speed, self.y)
        elif in_direction == Direction.RIGHT:
            return (self.x + self.speed, self.y)

    def check_collision_in_direction(self, in_direction: Direction):
        desired_position = self.calculate_position(in_direction)
        if in_direction == Direction.NONE: return False, desired_position
        return self.collides_with_wall(desired_position), desired_position

    def set_position(self, nx, ny):
        #print(f"Setting to {nx}, {ny}")
        self.x = nx
        self.y = ny

    def tick(self):
        pass

    def target_reached(self):
        pass

    def automatic_move(self, direction: Direction):
        pass

    def get_shape(self):
        #print(f"Shape: {self.x, self.y, self.size}")
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self):
        rectangle = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(self.surface, self.color, rectangle, border_radius=4)

    def set_direction(self, in_direction):
        self.current_direction = in_direction


class Ghost(MovableObject):
    def __init__(self, scene, x, y, size: int, color, speed):
        super().__init__(scene, x * size, y * size, size, color, speed)
        self.score = 200


class Hero(MovableObject):
    def __init__(self, scene, x, y, size: int, speed, offset=5):
        super().__init__(scene, x * size, y * size, size, speed)
        self.offset = offset
        self.image = pygame.image.load('assets/pacman.png')

    def set_direction(self, direction):
        self.current_direction = direction

    def tick(self):
        collision_status, position = self.check_collision_in_direction(self.current_direction)

        if collision_status:
            self.current_direction = self.previous_direction
        self.automatic_move(self.current_direction)
        self.previous_direction = self.current_direction

        self.cookie_pickup()

    def automatic_move(self, direction: Direction):
        collision_status, position = self.check_collision_in_direction(direction)

        if not collision_status:
            self.set_position(position[0], position[1])

    def draw(self):
        self.image = pygame.transform.scale(self.image, (self.size - 0.02, self.size - 0.02))
        self.surface.blit(self.image, self.get_shape())

    def cookie_pickup(self):
        collision_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        cookies = self.controller.cookies
        for cookie in cookies:
            collides = collision_rect.colliderect(cookie.get_shape())
            if collides and cookie in self.controller.game_objects:
                self.controller.game_objects.remove(cookie)
                self.controller.score += cookie.score
                cookies.remove(cookie)

        if len(cookies) == 0:
            self.controller.regenerate_flag = True
