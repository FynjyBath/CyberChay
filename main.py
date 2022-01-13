import pygame
import os
import sys
import random
import time

player_group = pygame.sprite.Group()
flying_objects = pygame.sprite.Group()
stars = pygame.sprite.Group()
fun_stars = pygame.sprite.Group()
progress_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
running = {'start': 1, 'game1': 0, 'game_over1': 0, 'game2': 0, 'game3': 0, 'story1': 0, 'story2': 0, 'story3': 0,
           'game_over3': 0, 'end': 0}
player = pygame.sprite.Sprite()
mistakes = 0
close_cards = pygame.sprite.Group()
now_cards = pygame.sprite.Group()
open_cards = pygame.sprite.Group()
chainik_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(name):
    name = os.path.join('data', name)
    f = open(name, 'r')
    return [i.strip('\n') for i in f.readlines()]


class FunStar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, fun_stars)
        self.image = load_image('star.png')
        s = random.randint(30, 60)
        self.image = pygame.transform.scale(self.image, (s, s))
        self.rect = pygame.Rect(x, y, s, s)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


def run_start():
    Border(5, 5, w - 5, 5)
    Border(5, h - 5, w - 5, h - 5)
    Border(5, 5, 5, h - 5)
    Border(w - 5, 5, w - 5, h - 5)
    for i in range(30):
        FunStar(random.randint(50, w - 50), random.randint(50, h - 50))

    fon = pygame.transform.scale(load_image('1fon.jpg'), (w, h))
    while running['start']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running['start'] = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                running['start'] = False
                running['story1'] = True
            if keys[pygame.K_ESCAPE]:
                for i in running.keys():
                    running[i] = 0
        screen.blit(fon, (0, 0))
        fun_stars.update()
        fun_stars.draw(screen)

        f = open('data\count.txt')
        kol = f.readline().strip()
        f.close()

        font = pygame.font.Font('data\segoeprint.ttf', 90)
        text = font.render("Всего заработано " + kol + " кг чая.", True, 'green')
        text_x = w // 2 - text.get_width() // 2
        text_y = h // 2 - 40
        screen.blit(text, (text_x, text_y))

        pygame.display.flip()
        clock.tick(30)


def run_story1():
    for el in all_sprites:
        el.kill()

    fon = pygame.transform.scale(load_image('story1.jpg'), (w, h))
    while running['story1']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running['story1'] = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                running['story1'] = False
                running['game1'] = True
            if keys[pygame.K_ESCAPE]:
                for i in running.keys():
                    running[i] = 0
        screen.blit(fon, (0, 0))
        pygame.display.flip()
        clock.tick()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = load_image('player0.png')
        x, y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (x * (h - 30) / 3 / y, (h - 30) / 3))
        self.rect = self.image.get_rect().move(30, 30 + (h - 30) / 3)
        self.mask = pygame.mask.from_surface(self.image)
        self.flag = 0

    def update(self):
        self.image = load_image('player' + str(self.flag) + '.png')
        x, y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (x * (h - 30) / 3 / y, (h - 30) / 3))
        if self.flag == 0:
            self.rect.y += 1
        elif self.flag == 1:
            self.rect.y -= 1
        elif self.flag == 2:
            self.rect.y -= 1
        else:
            self.rect.y += 1
        self.flag = (self.flag + 1) % 4


class FlyingObject(pygame.sprite.Sprite):
    def __init__(self, name, ind):
        super().__init__(flying_objects, all_sprites)

        self.orig = load_image('object' + name + '.png')
        x, y = self.orig.get_size()
        self.orig = pygame.transform.scale(self.orig, ((h - 30) / 3, (h - 30) / 3))

        self.angle = 0
        self.image = pygame.transform.rotate(self.orig, self.angle)
        self.xy = [w, 30 + (h - 30) / 3 * ind]
        self.rect = self.image.get_rect().move(self.xy[0], self.xy[1])
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta):
        if self.xy[0] <= -h / 3:
            self.kill()
            return
        self.angle = (self.angle + 0.5) % 360
        x, y = self.orig.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (x, 0), (x, -y), (0, -y)]]
        box_rotate = [p.rotate(self.angle) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
        pivot = pygame.math.Vector2(x / 2, -y / 2)
        pivot_rotate = pivot.rotate(self.angle)
        pivot_move = pivot_rotate - pivot
        pos = (self.xy[0] + min_box[0] - pivot_move[0], self.xy[1] - max_box[1] + pivot_move[1])

        self.image = pygame.transform.rotate(self.orig, self.angle)
        self.xy[0] -= 270 * delta / 1000
        self.rect = self.image.get_rect().move(pos[0], pos[1])
        self.mask = pygame.mask.from_surface(self.image)

        if pygame.sprite.collide_mask(self, player):
            running['game1'] = False
            running['game_over1'] = True


class ProgressBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(progress_group, all_sprites)
        self.x = 0
        pygame.draw.rect(screen, (128, 0, 255), (w / 3, 10, w / 3 * self.x, 10))
        pygame.draw.rect(screen, 'white', (w / 3, 10, w / 3, 10), 2)

    def update(self, x):
        self.x = x
        pygame.draw.rect(screen, (128, 0, 255), (w / 3, 10, w / 3 * self.x, 10))
        pygame.draw.rect(screen, 'white', (w / 3, 10, w / 3, 10), 2)


class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(stars, all_sprites)
        self.image = load_image('star.png')
        s = random.randint(20, 50)
        self.image = pygame.transform.scale(self.image, (s, s))
        self.rect = self.image.get_rect().move(random.randint(1, w), random.randint(1, h))
        self.v = random.randint(100, 360)

    def update(self, delta):
        if self.rect.x <= -100:
            self.rect.x = w
            self.rect.y = random.randint(1, h)
            self.v = random.randint(100, 360)
        self.rect = self.rect.move(-self.v * delta / 1000, 0)


def run_game1():
    level = load_level('level' + str(random.randint(1, 3)) + '.txt')

    for el in all_sprites:
        el.kill()

    global player
    player = Player()
    bar = ProgressBar()
    for _ in range(10):
        Star()

    now = 0
    yet = -1
    fon_pos = [0, 0]
    fon = pygame.transform.scale(load_image('2fon.jpg'), (2 * w + 100, h))
    delta = 0
    while running['game1']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running['game1'] = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                if 27 <= player.rect.y - (h - 30) / 3 <= 33 + (h - 30) / 3 * 2:
                    player.rect.y -= h / 3
            if keys[pygame.K_DOWN]:
                if 27 <= player.rect.y + (h - 30) / 3 <= 33 + (h - 30) / 3 * 2:
                    player.rect.y += h / 3
            if keys[pygame.K_ESCAPE]:
                for i in running.keys():
                    running[i] = 0

        screen.blit(fon, fon_pos)
        fon_pos[0] -= 50 * delta / 1000
        if fon_pos[0] <= -w + 10:
            fon_pos[0] = 0

        stars.update(delta)
        stars.draw(screen)
        player_group.draw(screen)
        flying_objects.update(delta)
        flying_objects.draw(screen)
        bar.update((now / h) / len(level[0]))
        player.update()

        if int(now // h) != yet:
            try:
                for i in range(3):
                    if level[i][int(now // h)] != 'x':
                        FlyingObject(level[i][int(now // h)], i)
                yet = int(now // h)
            except Exception:
                running['game1'] = False
                running['story2'] = True
        now += 270 * delta / 1000

        pygame.display.flip()
        delta = clock.tick()


def game_over1():
    fon = pygame.transform.scale(load_image('game_over1.png'), (w, h + 10))
    pos = [0, -h]
    delta = 0
    while running['game_over1']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running['game_over1'] = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                running['game_over1'] = False
                running['game1'] = True
            if keys[pygame.K_ESCAPE]:
                for i in running.keys():
                    running[i] = 0
        screen.blit(fon, pos)
        if pos[1] < 0:
            pos[1] += 360 * delta / 1000
        pygame.display.flip()
        delta = clock.tick()


def run_story2():
    fon = pygame.transform.scale(load_image('story2.jpg'), (w, h))
    while running['story2']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running['story2'] = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                running['story2'] = False
                running['game2'] = True
            if keys[pygame.K_ESCAPE]:
                for i in running.keys():
                    running[i] = 0
        screen.blit(fon, (0, 0))
        pygame.display.flip()
        delta = clock.tick()


class CloseCard(pygame.sprite.Sprite):
    def __init__(self, i, j, x, y, lx, ly):
        super().__init__(close_cards, all_sprites)
        self.image = load_image('card.png')
        self.image = pygame.transform.scale(self.image, (lx, ly))
        self.rect = self.image.get_rect().move(x, y)
        self.i = i
        self.j = j


class NowCard(pygame.sprite.Sprite):
    def __init__(self, i, j, x, y, name, lx, ly):
        super().__init__(now_cards, all_sprites)
        self.image = load_image(name)
        self.image = pygame.transform.scale(self.image, (lx, ly))
        self.rect = self.image.get_rect().move(x, y)
        self.i = i
        self.j = j


class OpenCard(pygame.sprite.Sprite):
    def __init__(self, i, j, x, y, name, lx, ly):
        super().__init__(open_cards, all_sprites)
        self.image = load_image(name)
        self.image = pygame.transform.scale(self.image, (lx, ly))
        self.rect = self.image.get_rect().move(x, y)
        self.i = i
        self.j = j


def run_game2():
    fon = pygame.transform.scale(load_image('3fon.jpg'), (w, h))

    rx, ry = 0.065104167 * w, 0.1157407 * h
    kx, ky = 6, 2
    lx, ly = (w - 2 * rx + 50) / kx, (h - 2 * ry + 50) / ky

    names = []
    for i in range(1, kx * ky // 2 + 1):
        names.append('card' + str(i) + '.png')
        names.append('card' + str(i) + '.png')
    random.shuffle(names)

    for i in range(ky):
        for j in range(kx):
            CloseCard(i, j, rx + j * lx, ry + i * ly, lx - 50, ly - 50)

    global mistakes
    mistakes = 0
    flag = 0
    ost = kx * ky
    while running['game2']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running['game2'] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                cont = 1
                for card in now_cards:
                    if card.rect.collidepoint(event.pos):
                        cont = 0
                for card in open_cards:
                    if card.rect.collidepoint(event.pos):
                        cont = 0
                if cont == 0:
                    continue
                now = [0, 0]
                now1 = [0, 0]
                for card in close_cards:
                    if card.rect.collidepoint(event.pos):
                        now = [card.rect.x, card.rect.y]
                        now1 = [card.i, card.j]
                if now != [0, 0]:
                    NowCard(now1[0], now1[1], now[0], now[1], names[int(now1[0] * kx + now1[1])], lx - 50, ly - 50)
                    now_cards.draw(screen)
                    pygame.display.flip()
                    flag += 1
                    if flag == 2:
                        time.sleep(1)
                        p = []
                        for card in now_cards:
                            p.append([card.i, card.j, card.rect.x, card.rect.y])
                        for card in now_cards:
                            card.kill()
                        if names[p[0][0] * kx + p[0][1]] == names[p[1][0] * kx + p[1][1]]:
                            OpenCard(p[0][0], p[0][1], p[0][2], p[0][3],
                                     names[p[0][0] * kx + p[0][1]], lx - 50, ly - 50)
                            OpenCard(p[1][0], p[1][1], p[1][2], p[1][3],
                                     names[p[1][0] * kx + p[1][1]], lx - 50, ly - 50)
                            ost -= 2
                        else:
                            mistakes += 1
                        flag = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                for i in running.keys():
                    running[i] = 0
        if ost == 0:
            running['game2'] = False
            running['story3'] = True
            for i in all_sprites:
                i.kill()
        screen.blit(fon, (0, 0))
        close_cards.draw(screen)
        now_cards.draw(screen)
        open_cards.draw(screen)
        pygame.display.flip()
        delta = clock.tick()


def run_story3():
    fon = pygame.transform.scale(load_image('story3.jpg'), (w, h))
    while running['story3']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running['story3'] = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                running['story3'] = False
                running['game3'] = True
            if keys[pygame.K_ESCAPE]:
                for i in running.keys():
                    running[i] = 0
        screen.blit(fon, (0, 0))

        font = pygame.font.Font('data\segoeprint.ttf', 90)
        if mistakes <= 8:
            text = font.render("Вы ошиблись " + str(mistakes) + " раз(а)", True, 'green')
        else:
            text = font.render("Вы ошиблись " + str(mistakes) + " раз(а)", True, 'red')
        text_x = w // 2 - text.get_width() // 2
        text_y = h // 3 - 100
        screen.blit(text, (text_x, text_y))

        font1 = pygame.font.Font('data\segoeprint.ttf', 90)
        text1 = font.render("Получено " + str(80 // max(1, mistakes)) + " кг чая.", True, 'green')
        text_x1 = w // 2 - text1.get_width() // 2
        text_y1 = h // 3 + 50
        screen.blit(text1, (text_x1, text_y1))

        pygame.display.flip()
        delta = clock.tick()


class Laser(pygame.sprite.Sprite):
    def __init__(self, ind):
        super().__init__(laser_group, all_sprites)

        self.image = load_image('laser.png')
        x, y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, ((h - 30) / 3, (h - 30) / 3))
        self.rect = self.image.get_rect().move(w - (h - 30) / 3 * 1.2706624605678 - 30, 30 + (h - 30) / 3 * ind)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta):
        if self.rect.x <= -h / 3:
            self.kill()
            return
        self.rect.x -= 360 * delta / 1000
        if pygame.sprite.collide_mask(self, player):
            running['game3'] = False
            running['game_over3'] = True


class Chainik(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(chainik_group, all_sprites)
        self.image = load_image('chainik1.png')
        x, y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, ((h - 30) / 3 * 1.2706624605678, (h - 30) / 3))
        self.ind = 1
        self.xy = [w - (h - 30) / 3 * 1.2706624605678 - 10, 30 + (h - 30) / 3 * self.ind]
        self.rect = self.image.get_rect().move(self.xy[0], self.xy[1])

    def update(self, flag):
        if flag == 0:
            self.image = load_image('chainik1.png')
            x, y = self.image.get_size()
            self.image = pygame.transform.scale(self.image, ((h - 30) / 3 * 1.2706624605678, (h - 30) / 3))
            self.ind = random.randint(0, 2)
            self.xy = [w - (h - 30) / 3 * 1.2706624605678 - 10, 30 + (h - 30) / 3 * self.ind]
            self.rect = self.image.get_rect().move(self.xy[0], self.xy[1])
        elif flag == 1:
            self.image = load_image('chainik2.png')
            x, y = self.image.get_size()
            self.image = pygame.transform.scale(self.image, ((h - 30) / 3 * 1.2706624605678, (h - 30) / 3))
            self.ind = int(player.rect.y // ((h - 30) / 3))
            self.xy = [w - (h - 30) / 3 * 1.2706624605678 - 10, 30 + (h - 30) / 3 * self.ind]
            self.rect = self.image.get_rect().move(self.xy[0], self.xy[1])
        else:
            Laser(int((self.rect.y - 30) // ((h - 30) / 3)))


def run_game3():
    for el in all_sprites:
        el.kill()

    global player
    player = Player()
    bar = ProgressBar()
    for _ in range(10):
        Star()
    Chainik()

    now = 0
    flag = 0
    last = 0
    fon_pos = [0, 0]
    fon = pygame.transform.scale(load_image('2fon.jpg'), (2 * w + 100, h))
    delta = 0
    while running['game3']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running['game3'] = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                for i in running.keys():
                    running[i] = 0
            if keys[pygame.K_UP]:
                if 27 <= player.rect.y - (h - 30) / 3 <= 33 + (h - 30) / 3 * 2:
                    player.rect.y -= h / 3
            if keys[pygame.K_DOWN]:
                if 27 <= player.rect.y + (h - 30) / 3 <= 33 + (h - 30) / 3 * 2:
                    player.rect.y += h / 3

        screen.blit(fon, fon_pos)
        fon_pos[0] -= 50 * delta / 1000
        if fon_pos[0] <= -w + 10:
            fon_pos[0] = 0

        stars.update(delta)
        stars.draw(screen)
        player_group.draw(screen)
        bar.update(now / 10000)
        player.update()

        if now / 10000 >= 1:
            running['game3'] = False
            running['end'] = True

        if flag == 0:
            if last >= h / 6 * 4:
                chainik_group.update(1)
                last = 0
                flag = 1
        elif flag == 1:
            if last >= h / 6:
                chainik_group.update(2)
                last = 0
                flag = 2
        else:
            if last >= h / 6:
                chainik_group.update(0)
                last = 0
                flag = 0
        chainik_group.draw(screen)
        laser_group.update(delta)
        laser_group.draw(screen)

        last += 270 * delta / 1000
        now += 270 * delta / 1000

        pygame.display.flip()
        delta = clock.tick()


def game_over3():
    fon = pygame.transform.scale(load_image('game_over3.jpg'), (w, h + 10))
    pos = [0, -h]
    delta = 0
    while running['game_over3']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running['game_over3'] = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                running['game_over3'] = False
                running['game3'] = True
            if keys[pygame.K_ESCAPE]:
                for i in running.keys():
                    running[i] = 0
        screen.blit(fon, pos)
        if pos[1] < 0:
            pos[1] += 360 * delta / 1000
        pygame.display.flip()
        delta = clock.tick()


def run_end():
    f = open('data\count.txt')
    kol = int(f.readline().strip()) + 80 // max(1, mistakes)
    f.close()
    f = open('data\count.txt', 'w')
    print(kol, file=f)
    f.close()

    fon = pygame.transform.scale(load_image('end.jpg'), (w, h))
    while running['end']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running['end'] = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                for i in running.keys():
                    running[i] = 0
            if keys[pygame.K_SPACE]:
                running['end'] = False
                running['start'] = True
        screen.blit(fon, (0, 0))
        pygame.display.flip()
        delta = clock.tick()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('')

    infoObject = pygame.display.Info()
    size = w, h = infoObject.current_w, infoObject.current_h
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

    clock = pygame.time.Clock()

    while 1 in running.values():
        if running['start']:
            run_start()
        if running['story1']:
            run_story1()
        if running['game1']:
            run_game1()
        if running['game_over1']:
            game_over1()
        if running['story2']:
            run_story2()
        if running['game2']:
            run_game2()
        if running['story3']:
            run_story3()
        if running['game3']:
            run_game3()
        if running['game_over3']:
            game_over3()
        if running['end']:
            run_end()
    pygame.quit()
