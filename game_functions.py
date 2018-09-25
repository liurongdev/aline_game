import pygame
import sys
from bullet import Bullet
from alien import  Alien
from time import sleep

def check_keyup_event(event,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    elif event.key == pygame.K_LEFT:
        ship.move_left = False
    elif event.key == pygame.K_SPACE:
        bullets.is_continue_fire = False



def check_keydown_event(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    elif event.key == pygame.K_LEFT:
        ship.move_left = True
    elif event.key == pygame.K_SPACE:
        bullets.is_continue_fire=True
        fire_bullets(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()



def fire_bullets(ai_settings,screen,ship,bullets):
    if bullets.is_continue_fire and len(bullets)<ai_settings.bullets_allowed:
        new_bullet = Bullet(screen,ai_settings,ship)
        bullets.add(new_bullet)
        bullets.update()

        print("-->" + str(len(bullets)))






def check_events(ai_settings,screen,states,sb,button,ship,aliens,bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, states,sb, button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_settings, screen, ship, bullets)
        elif event.type== pygame.KEYUP:
            check_keyup_event(event,ship,bullets)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, button,
                              ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings,screen,states,sb,button,ship,aliens,bullets,mouse_x,mouse_y):
    button_click = button.rect.collidepoint(mouse_x,mouse_y)
    if button_click and not states.game_active:
        pygame.mouse.set_visible(False)

        states.restart_stat()
        states.game_active = True

        sb.prep_high_score()
        sb.prep_level()
        sb.prep_score()
        sb.prep_ships()

        ai_settings.initialize_dynamic_settings()

        aliens.empty()
        bullets.empty()

        #创建一波新的外星人
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()










def update_screen(ai_settings,screen,status,sb,ship,aliens,bullets,button):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.bitme()
    #alien.blitme()
    aliens.draw(screen)

    sb.show_score()


    if not status.game_active :
        button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def bullet_update(bullets):
    """删除在屏幕之外的子弹"""
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    print(len(bullets))


def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人人群"""

    alien=Alien(ai_settings,screen)
    alien_numbers=get_numbers_alien_x(ai_settings,alien.rect.width)

    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(alien_numbers):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def get_numbers_alien_x(ai_settings,alien_width):
    """获取每一行可以创建的外星人数量"""
    valiables_x = ai_settings.screen_width - 2 * alien_width
    numbers = int(valiables_x / (2 * alien_width))
    return numbers


def create_alien(ai_settings,screen,aliens,alien_number,alien_row_number):
    alien=Alien(ai_settings,screen)
    alien_width=alien.rect.width
    alien.x=alien_width + 2 *alien_number*alien_width
    alien.rect.x=float(alien.x)
    alien.rect.y=alien.rect.height + 2* alien.rect.height* alien_row_number
    aliens.add(alien)


def get_number_rows(ai_settings,ship_height,alien_height):
    """获取总共有多少行外星人"""
    space_heith=ai_settings.screen_hight - 3*alien_height -ship_height
    return int(space_heith / (2* alien_height))

def check_fleet_edges(ai_settings,aliens):
    """检测到有外星人到达边缘时候采取的措施"""
    for alien in aliens.sprites():
        if alien.check_edages():
            change_fleet_direction(ai_settings,aliens)
            break;

def change_fleet_direction(ai_settings,aliens):
    """改变外星人的走向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings,states,screen,sb,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
       ship_hit(ai_settings,states,screen,sb,ship,aliens,bullets)

    check_aliens_bottom(ai_settings, states, screen,sb, ship, aliens, bullets)

def check_aliens_bottom(ai_settings,states,screen,sb,ship,aliens,bullets):
    screen_rect=screen.get_rect()
    for aliens in aliens.sprites():
        if aliens.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, states, screen,sb,ship, aliens, bullets)
            break


def ship_hit(ai_settings,states,screen,sb,ship,aliens,bullets):
    if states.ships_left >0 :
        states.ships_left -=1
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)

        ship.center_ship()

        sleep(1.5)
    else:
        states.game_active=False
        pygame.mouse.set_visible(True)



def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <=0:
            bullets.remove(bullet)


    check_bullet_alien_collisions(ai_settings, screen, stats,sb,ship, aliens, bullets)



def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """检测是否有子弹和外星人碰撞,返回的是一个字典"""
    collections = pygame.sprite.groupcollide(aliens, bullets, True, True)

    if collections:
        for aliens in collections.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)


    # 如果没有外星人，则新生成一波外星人
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        #提高等级
        stats.level+=1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)



def check_high_score(stats,sb):
    if stats.score > stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()
