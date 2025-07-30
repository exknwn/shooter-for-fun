from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.y, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            lost += 1

class Netral(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(30, win_height - 30)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('hambuh buh')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

snip = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, win_height - 80), -40, 80, 50, randint(1,3))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Netral('asteroid.png', randint(30, win_height - 30), -40, 80, 50, randint(4,7))
    asteroids.add(asteroid)

bullets = sprite.Group()

score = 0
lost = 0

font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 80)

win = font2.render('you win', 1, (255, 255, 255))
lose = font2.render('you loser', 1, (180, 0 , 0))

game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                snip.fire()

    if finish == False:
        snip.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        window.blit(background, (0, 0))
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        snip.reset()
        text = font1.render(f'Счёт: {score}', 1, (255, 255, 255))
        text_lose = font1.render(f'Пропущено: {lost}', 1, (255, 255, 255))
        window.blit(text, (10, 20))
        window.blit(text_lose, (10, 50))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for s in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_height - 80), -40, 80, 50, randint(1,3))
            monsters.add(monster)

        omg = sprite.spritecollide(snip, monsters, False)
        omg2 = sprite.spritecollide(snip, asteroids, False)

        if omg or omg2 or lost >= 10:
            finish = True
            window.blit(lose, (200, 200))
        if score >= 20:
            finish = True
            window.blit(win, (200, 200))
    else:
        score = 0
        lost = 0
        for b in bullets:
            b.kill()

        for m in monsters:
            m.kill()

        for a in asteroids:
            a.kill()

        time.delay(3000)

        for i in range(5):
            monster = Enemy('ufo.png', randint(80, win_height - 80), -40, 80, 50, randint(1,3))
            monsters.add(monster)

        for q in range(3):
            asteroid = Netral('asteroid.png', randint(30, win_height - 30), -40, 80, 50, randint(4,7))
            asteroids.add(asteroid)
        
        finish = False
 
    display.update()
    clock.tick(FPS)