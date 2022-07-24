import pygame
from ship import Ship


# 写个飞船的新模式

class Ship_modile_one(Ship):
    def __init__(self, ai_game):
        super().__init__(ai_game)

        # 加载飞船图像并获取其外外接矩形
        self.image = pygame.image.load("images/")
        self.new_bullets = ai_game.bu
