import pygame as pg
import random
pg.init()
win_width, win_height = 800, 600
window = pg.display.set_mode((win_width, win_height))
pg.display.set_caption("Шутер")
class GameSprite:
    def __init__(self, image, x, y, width, height, speed):
        self.width = width
        self.height = height
        self.speed = speed
        self.image = pg.transform.scale(pg.image.load(image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def control(self):
        keys = pg.key.get_pressed()
        if keys [pg.K_a]and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys [pg.K_d]and self.rect.x < 700:
            self.rect.x += self.speed


class Enemy(GameSprite):
    def spawn(self):
        self.rect.y = 0
        self.rect.x = random.randint(0, 700)
    def move(self):
        global miss_enemy
        if self.rect.y < 600:
            self.rect.y += self.speed
        else:
            miss_enemy += 1
            self.spawn()
    def dead(self):
        global bullets, score
        for i in bullets:
            if pg.sprite.collide_rect(self, i):
                score +=1
                self.spawn()
                bullets.remove(i)

class Bullet(GameSprite):
    def move(self):
        self.rect.y -= self.speed
class Boss(GameSprite):
    def __init__(self, image, x, y, width, height, speed, health, direction):
        super().__init__(image, x, y, height, width, speed)
        self.health = health
        self.direction = direction
    def move(self):
        global count_animation
        if self.direction == 1:
            self.rect.x += self.speed
        if self.direction == 2:
            self.rect.x -= self.speed
        if self.rect.x > 600:
            self.direction = 2
        if self.rect.x < 0:
            self.direction = 1

        self.image = pg.transform.scale(pg.image.load(f"image/boss/{count_animation}.gif"), (self.width, self.height))
        count_animation += 1
        if count_animation == 19:
            count_animation = 0
    def dead(self):
        global bullets
        for i in bullets:
            if pg.sprite.collide_rect(self, i):
                bullets.remove(i)
                self.health -= 1
        try:
            hp = GameSprite("image/kvadrat.png", 0, 0, self.health * 3, 20, 0)
            hp.reset()
        except:
            pass
boss = Boss("image/boss/0.gif", 0, 0, 200, 200, 4, 250, 1)
player = Player("image/Hero.png", 350, 500, 100, 100, 5)
enemies = []
bullets = []
enemie = []
for i in range(3):
    enemie.append(Enemy("image/nlo.webp", random.randint(0,700), 0, 100, 100, 5))
for i in range(4):
    enemies.append(Enemy("image/Enemy.png", random.randint(0, 700), 0, 100, 100, 3))
back = GameSprite("image/fon.jpg", 0, 0, 800, 600, 0)
game = True
miss_enemy = 0
score = 0
count_animation = 0
game_over = "image/youw.jpg"
while game:
    pg.time.Clock().tick(100)
    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
        if i.type == pg.MOUSEBUTTONDOWN:
            bullets.append(Bullet("image/pula.png", player.rect.x + player.width//2, player.rect.y, 10, 25, 7))
    back.reset()
    player.reset()
    player.control()
    if score > 30:
        for i in enemie:    
            i.reset()
            i.move()
            i.dead()
    if score > 50:
        boss.reset()
        boss.move()
        boss.dead()
    for i  in enemies:
        i.reset()
        i.move()
        i.dead()
    for i in bullets:
        i.reset()
        i.move()
    if boss.health <= 0:
        game = False
    if miss_enemy >= 15:
        game_over = "image/gameover.jpg"
        game = False
    label = pg.font.SysFont("Exo", 27).render(f"kills enemys: {score}", True, "red")
    window.blit(label,(20, 20))
    label2 = pg.font.SysFont("Bebas Neue", 27).render(f"miss enemys: {miss_enemy}", True, "red")
    window.blit(label2,(20, 50))
    pg.display.flip()
bg = GameSprite(game_over, 0, 0, 800, 600, 0)
while True:
    pg.time.Clock().tick(100)
    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
    bg.reset()
    pg.display.flip()