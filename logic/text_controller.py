import pygame


class TextBlock:
    def __init__(self, surface, x, y, size, font, base_text=''):
        self.surface = surface
        self.size = size
        self.font = font
        self.x = x
        self.y = y
        self.text_render = self.font.render(base_text, True, (0, 0, 0))

    def tick(self, text):
        pass

    def draw(self):
        text_rectangle = self.text_render.get_rect()
        text_rectangle.center = (self.x + self.size[0] // 2, self.y + self.size[1] // 2)
        self.surface.blit(self.text_render, text_rectangle)


class ChangingTextBlock(TextBlock):
    def __init__(self, surface, x, y, size, font):
        super().__init__(surface, x, y, size, font)

    def tick(self, text):
        self.text_render = self.font.render(str(text), True, (0, 0, 0))


class ScoreController(TextBlock):
    def __init__(self, surface, x, y, size, font):
        super().__init__(surface, x, y, size, font)
        self.score = 0

    def tick(self, score):
        self.score = score
        self.text_render = self.font.render(f"{self.score}", True, (0, 0, 0))


class HighScoreController(TextBlock):
    def __init__(self, surface, x, y, size, font):
        super().__init__(surface, x, y, size, font)
        self.high_score = 0

    def tick(self, score):
        if score > self.high_score: self.high_score = score
        self.text_render = self.font.render(f"{self.high_score}", True, (0, 0, 0))
