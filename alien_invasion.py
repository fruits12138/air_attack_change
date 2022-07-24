import sys
import pygame
from time import sleep
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

"还需要注意排版顺序，因为是从上往下执行的"


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # 调全屏的
        """ self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        """
        """为何每次set——modAe要（（）），括号里面含括号
        """
        pygame.display.set_caption("AlienInvasion")

        # 创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)
        # 创建存储游戏统计信息的实例
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        """self让ship调用全部alien——invasion的全部资源，类的基础参数运用"""
        # 设置背景色,bg = background
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # 创建一个按钮
        self.play_button = Button(self, "Play")

    def run_game(self):
        """开始游戏的主循环"""
        FPS = 600
        Clock = pygame.time.Clock()
        while True:
            self._check_events()
            """方法里调用方法赋值属性"""
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            Clock.tick(FPS)

    def _check_events(self):
        # 监视键盘和鼠标事件，事件就是玩家在键盘和鼠标的操作
        for event in pygame.event.get():
            """获取判断是否为sys.exit"""
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """点击PLAY重新开始，"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            # 重置游戏设置
            self.settings.initialize_dynamic_settings()

            # 飞船数量重置
            self.stats.reset_stats()
            self.stats.game_active = True

            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.ceter_ship()

            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """相应按键,event指的是get（）里面的"""
        if event.key == pygame.K_RIGHT:
            # 向右移动飞船。
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # 向右移动飞船。
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            # 向右移动飞船。
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            # 向右移动飞船。
            self.ship.moving_down = True



        elif event.key == pygame.K_q:
             sys.exit()

        elif event.key == pygame.K_SPACE:
            if self.ship.change_1 == False:
                self.ship.keyc = True
            elif self.ship.change_1 == True:
                self.ship.keyc = False
                self._fire_bullet()
        elif event.key == pygame.K_c:
            self.ship_model_change()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_c:
            self.ship.keyc=False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        # 更新子弹位置
        # 删除消失的子弹
        if self.ship.keyc == True:
            self._fire_bullet()
        elif self.ship.keyc == False:
            pass
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """相应子弹与外星人碰撞。"""
        # 检查是否有子弹击中了外星人。
        #   如果是，那么删除对应的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            """删除现有子弹，并创建新的外星人"""
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            """提升玩家等级"""
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """更新外星人群中所有外星人的位置"""
        self.aliens.update()
        self._check_fleet_edges()

        # 检测飞船与外星人的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            """print("Ship hit!!!")"""
            self._ship_hit()

        # 检查是否有外形人到达底端
        self._check_aliens_bottom()

    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人并计算能容纳多少个外星人
        # 外星人的间距为外星人宽度
        alien = Alien(self)
        """bullet 的创建模板"""
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算屏幕能容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # 创建第一个外星群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # 创建一个外星人比那个将其加入当前行
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """有外星人到达边缘采取的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_directions()
                break

    def _change_fleet_directions(self):
        """将整群外星人下移并改变方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """相应飞船被外星人撞到"""
        if self.stats.ships_left > 0:
            # 将ship_left -1
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人，并将飞船房贷屏幕底端中央
            self._create_fleet()
            self.ship.ceter_ship()
            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕底部"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船一样处理
                self._ship_hit()
                """只执行一次的break"""
                break

    def _update_screen(self):
        # 更新屏幕上的图像，并切换到新屏幕，包括飞船屏幕更新
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 显示分数
        """每秒钟都会显示分数"""
        self.sb.show_score()

        # 如果游戏处于非活动状态就会之按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见。
        pygame.display.flip()


#飞船的形态
    def ship_model_change(self):
        if self.ship.change_1==True:
            self.ship.change_1=False
        elif self.ship.change_1==False:
            self.ship.change_1=True


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()



#        elif event.key == pygame.K_SPACE:
  #         self._fire_bullet()