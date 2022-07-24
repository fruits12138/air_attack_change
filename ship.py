import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """管理飞船的类"""

    def __init__(self, ai_game):
        super().__init__()
        """初始化飞船并设置其初始位置"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其外外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        # 这里就是图像加载
        self.rect = self.image.get_rect()
        """这里是矩形移动的图像获取的位置坐标"""

        # 对于没搜飞船，都将其放在屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom
        # 在飞船的属性x中存储小数值
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # 飞船形态
        self.change_1 = False
        self.change_2 = False
        self.change_3 = False

        self.keyc=False

    def update(self):
        """根据移动标志调整飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        # 根据self。x更新rect对象
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """指定位置绘制飞船"""
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        """rect指的是矩形，blit是传送的意思"""

    def ceter_ship(self):
        """让飞船位居屏幕地段中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        """重置用于跟踪过子弹的x，这个一定不能忘，属性重置"""
        self.x = float(self.rect.x)

