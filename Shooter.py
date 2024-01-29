from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
    def fire(self):
        bull = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15, 15, 25)
        bulls.add(bull)
        
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(0, 700)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

window = display.set_mode((700, 500))
display.set_caption('Шутер')

back = transform.scale(image.load('galaxy.jpg'), (700, 500))

font.init()
mixer.init()
mixer.music.load('space.ogg')
fire = mixer.Sound('fire.ogg')

mixer.music.play()

hero = Player('rocket.png', 200, 390, 10, 80, 100)

score = 0
live = 3
rel_time = False #Перезарядка
num_fire = 0

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(0, 700), -40, randint(1,6), 80, 50)
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(0, 700), -40, randint(1,6), 80, 50)
    asteroids.add(asteroid)

bulls = sprite.Group()


game = True
finish = False

lose = font.Font(None, 45).render('YOU LOSE!', True, (235, 52, 58))
win = font.Font(None, 45).render('YOU WIN!', True, (22, 245, 29))


while game:

    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire.play()
                    hero.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True


    if not finish:
        window.blit(back, (0, 0))

        text_lose = font.Font(None, 40).render('Счёт: ' + str(score), True, (3, 236, 252))
        text = font.Font(None, 40).render('Пропущено: ' + str(lost), True, (3, 236, 252))
        window.blit(text, (20, 20))
        window.blit(text_lose, (20, 60))

        hero.reset()
        monsters.draw(window)
        monsters.update()
        
        asteroids.draw(window)
        asteroids.update()

        hero.update()
        bulls.update()
        bulls.draw(window)

        if rel_time == True:
            new_time = timer()
        
            if new_time - last_time < 3:
                text_t = font.Font(None, 35).render('Подождите, идет перезарядка...', True, (235, 52, 58))
                window.blit(text_t, (250, 420))
            else:
                num_fire = 0
                rel_time = False

        sprites_list = sprite.groupcollide(monsters, bulls, True, True)
        for _ in sprites_list:
            score += 1
            monster = Enemy('ufo.png', randint(0, 700), -40, randint(3,8), 80, 50)
            monsters.add(monster)
        
        if sprite.spritecollide(hero, asteroids, False) or sprite.spritecollide(hero, monsters, False):
            sprite.spritecollide(hero, monsters, True)
            sprite.spritecollide(hero, asteroids, True)
            live -= 1

        if score >= 10:
            finish = True
            window.blit(win, (250, 250))

        if live == 0 or lost >= 5:
            finish = True
            window.blit(lose, (250, 250))

        text_live = font.Font(None, 40).render('Кол-во жизней: ' + str(live), True, (3, 236, 252))
        window.blit(text_live, (20, 100))
        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        live = 3

        for i in bulls:
            i.kill()

        for m in monsters:
            m.kill()

        for a in asteroids:
            a.kill()
        
        time.delay(3000)

        for i in range(4):
            monster = Enemy('ufo.png', randint(0, 700), -40, randint(1,6), 80, 50)
            monsters.add(monster)
        
        for i in range(3):
            asteroid = Enemy('asteroid.png', randint(0, 700), -40, randint(1,6), 80, 50)
            asteroids.add(asteroid)

    time.delay(50)
