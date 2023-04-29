from pygame import*

from random import randint

from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, image1, speed, rect_x, rect_y, width,height):
        super().__init__()
        self.image = transform.scale(image.load(image1), (width,height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.width = width
        self.height = height

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

lost = 0
ale = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 700-self.width-5)
            lost += 1

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 3:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 700 - self.width + 30:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', -20, self.rect.centerx, self.rect.top,15,20)
        bullets.add(bullet)

bullets = sprite.Group()

enemys = sprite.Group()
enemy1 = Enemy('ufo.png', randint(2,2),randint(0, 700-150-5), 0, 100,65)
enemy2 = Enemy('ufo.png', randint(2,2),randint(0, 700-150-5), 0, 100,65)
enemy3 = Enemy('ufo.png', randint(2,2),randint(0, 700-150-5), 0, 100,65)
enemy4 = Enemy('ufo.png', randint(2,2),randint(0, 700-150-5), 0, 100,65)
enemy5 = Enemy('ufo.png', randint(2,2),randint(0, 700-150-5), 0, 100,65)

enemys.add(enemy1)
enemys.add(enemy2)
enemys.add(enemy3)
enemys.add(enemy4)
enemys.add(enemy5)

rocket = Player('rocket.png',12,300,400,200,100)
window = display.set_mode((700,500))
display.set_caption('Шутер')

font.init()
font1 = font.SysFont('Arial',40)
font2 = font.SysFont('Arial',60)

win = font2.render('Вы вязли Киев!',True,(255,255,255))
defeat = font2.render('Бюджет США закончился!',True,(255,0, 0))


background = transform.scale(image.load('galaxy.jpg'),(700,500))
game = True
fps = 60
clock = time.Clock()
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
fire = mixer.Sound('fire.ogg')

asteroids = sprite.Group()

for i in range(1, 3):
    asteroid = Enemy('asteroid.png', randint(30, 700 - 30), -40, 80, 50, randint(1, 3))
    asteroids.add(asteroid)


finish = False
rel_time = False
num_fire = -500

while game != False:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    fire.play()
                    rocket.fire()
                    num_fire = num_fire + 1

                if num_fire >= 10 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if finish != True:

        window.blit(background,(0,0))

        rocket.reset()
        rocket.update()

        enemys.draw(window)
        enemys.update()

        bullets.draw(window)
        bullets.update()

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 1:
                reload = font2.render('Ракеты закончились', 1, (150,0,0))
                window.blit(reload, (260,460))
            else:
                num_fire = 0
                rel_time = False

        sprites_list = sprite.groupcollide(enemys,bullets,True,True)
        for s in sprites_list:
            ale += 1
            enemy = Enemy('ufo.png', randint(3,3),randint(0, 700-150-5), 0, 100,65)
            enemys.add(enemy)

        if sprite.spritecollide(rocket,enemys,False):
            finish = True
            window.blit(defeat,(80,200))

        text_lost = font1.render('пропущено: ' + str(lost),True,(255,255,255))
        window.blit(text_lost, (3,3))

        text_lost = font1.render('уничтожено абрамсов: ' + str(ale),True,(255,255,255))
        window.blit(text_lost, (5,30))

        if lost >= 3:
            finish = True
            window.blit(defeat,(80,200))

        if ale >= 50  :
            finish = True
            window.blit(win,(180,200))


    display.update()
    clock.tick(60)

