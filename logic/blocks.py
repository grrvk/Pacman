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
    def __init__(self, game_screen, x, y, size: int, color=(33, 25, 81)):
        super().__init__(game_screen, x * size, y * size, size, color)
        self.shape = pygame.Rect(self.x, self.y, size, size)

    def draw(self):
        rectangle = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(self.surface, self.color, rectangle, border_radius=4)


class Heart(GameObject):
    def __init__(self, game_screen, x, y, size: int, color=(181, 193, 142)):
        super().__init__(game_screen, x * size, y * size, size, color)
        self.image = pygame.image.load('assets/heart.png')

    def draw(self):
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.surface.blit(self.image, self.get_shape())


class Cherry(GameObject):
    def __init__(self, game_screen, x, y, size: int, color=(181, 193, 142)):
        super().__init__(game_screen, x * size, y * size, size, color)
        self.image = pygame.image.load('assets/cherry.png')
        self.score = 50

    def draw(self):
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.surface.blit(self.image, self.get_shape())


class Door(Wall):
    def __init__(self, game_screen, x, y, size: int, color=(0,0,0)):
        super().__init__(game_screen, x * size, y * size, size, color)

    def draw(self):
        rectangle = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(self.surface, self.color, rectangle, border_radius=4)


class SmallCookie(GameObject):
    def __init__(self, game_screen, x, y, size: int, color=(255, 222, 77)):
        super().__init__(game_screen, x * size + size//2, y * size + size//2, size // 7, color)
        self.score = 10

    def draw(self):
        pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.size)


class Powerup(GameObject):
    def __init__(self, game_screen, x, y, size: int, color=(255, 222, 77)):
        super().__init__(game_screen, x * size + size//2, y * size + size//2, size // 3, color)
        self.score = 50

    def draw(self):
        pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.size)
