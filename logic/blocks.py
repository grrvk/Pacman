import pygame


class GameObject:
    def __init__(self, game_screen, x, y, size: int, color=(255, 0, 0)):
        self.size = size
        self.surface = game_screen
        self.y = y
        self.x = x
        self.color = color

    def draw(self):
        pass

    def tick(self):
        pass

    def get_shape(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)


class Wall(GameObject):
    def __init__(self, game_screen, x, y, size: int, color=(181, 193, 142)):
        super().__init__(game_screen, x * size, y * size, size, color)
        self.shape = pygame.Rect(self.x, self.y, size, size)

    def draw(self):
        rectangle = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(self.surface, self.color, rectangle, border_radius=4)


class Door(Wall):
    def __init__(self, game_screen, x, y, size: int, color=(247, 181, 202)):
        super().__init__(game_screen, x * size, y * size, size, color)


class SmallCookie(GameObject):
    def __init__(self, game_screen, x, y, size: int, color=(255, 222, 77)):
        super().__init__(game_screen, x * size + size//2, y * size + size//2, size // 7, color)
        self.score = 10

    def draw(self):
        pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.size)
