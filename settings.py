class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""

    def __init__(self):
        """初始化游戏的设置。"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船速度设置
        self.ship_speed = 5.0
        self.ship_limit = 5

        # 子弹设置
        self.bullet_speed = 1.5
        self.bullet_width = 3.0
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 90

        # 外星人设置
        self.alien_speed = 1.0
        self.fleet_drop_speed = 5
        # fleet_direction 为1表示向右移，为-1表示向左移
        self.fleet_direction = 1

        # 加快游戏节奏
        self.speedup_scale = 1.1
        # 外星人分数的提高速度
        self.score_scale = 1.5
        # 游戏开始的初始化
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ 初始化随游戏进行而变化的设置,重新初始化"""
        self.ship_speed = 1.5
        self.alien_speed = 3.0
        self.bullet_speed = 1.0
        """外星人舰队的整体方向"""
        self.fleet_direction = 1
        # 计分
        self.alien_points = 50

    def increase_speed(self):
        """提高游戏各方面速度设置"""
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        """为何不是整数因为乘数为1.5"""

