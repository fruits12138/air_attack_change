import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """显示得分信息的类"""

    def __init__(self, ai_game):
        """初始化显示得分涉及的属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 显示得分信息时的使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # 准备初始得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分进行渲染"""
        rounded_score = round(self.stats.score, -1)
        score_string = "{:,}".format(rounded_score)
        """千位符"""
        # score_string = str(self.stats.score)
        self.score_image = self.font.render(score_string, True, self.text_color, self.settings.bg_color)

        # 再右上角显示得分
        self.score_rect = self.score_image.get_rect()

        """记录版的初始位置"""
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高分渲染为图像，"""
        high_score = round(self.stats.high_score,-1)
        high_score_string = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_string, True, self.text_color, self.settings.bg_color)

        # 将最高分放到屏幕中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
        """很多属性赋值，并在最后达到屏幕上"""

    def check_high_score(self):
        """检验最高分是否出现"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """打印玩家等级"""
        level_string = str(self.stats.level)
        self.level_image = self.font.render(level_string, True, self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """打印飞船的剩余数量"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """展示分数"""
        self.screen.blit(self.score_image, self.score_rect)
        """显示分数并放到指定位置"""
        self.screen.blit(self.high_score_image, self.high_score_rect)
        """在屏幕上显示玩家等级"""
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)