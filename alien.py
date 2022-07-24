import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人"""

    def __init__(self, ai_game):
        """初始化外星人， 并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载外星人图像并设置rect的值
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 没一个外星人最初在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 储存外星人的精确位置
        self.x = float(self.rect.x)

    def check_edges(self):
        """检测alien是否撞到了边缘,如果在边缘就返回TRUE"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """向右移动外星人"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        """分开区分水平移动速度和垂直速度"""
        self.rect.x = self.x
