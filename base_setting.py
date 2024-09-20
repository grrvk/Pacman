import pygame


class GameRenderer:
    def __init__(self, in_width: int, in_height: int):
        pygame.init()
        self._width = in_width
        self._height = in_height
        self._screen = pygame.display.set_mode((in_width, in_height))
        self.font = pygame.font.SysFont('Arial', 40)
        pygame.display.set_caption('Pacman')
        self._clock = pygame.time.Clock()
        self._game_objects = []
        self._walls = []
        self._cookies = []
        self._hero = None
        self.run = True

    def tick(self, fps=60):
        while self.run:
            for game_object in self._game_objects:
                game_object.tick()
                game_object.draw()
            pygame.display.flip()
            self._clock.tick(fps)
            self._screen.fill((0, 0, 0))
            self.handle_event()
        print("Finished")
        pygame.quit()

    def add_game_object(self, obj):
        self._game_objects.append(obj)

    def add_wall(self, obj):
        self.add_game_object(obj)
        self._walls.append(obj)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
