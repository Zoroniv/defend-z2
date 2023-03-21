import pygame
import os
import random
import time

pygame.init()

WIDTH, HEIGHT= 1000,500
FPS= 60

pygame.display.set_caption("Defend Z")
win= pygame.display.set_mode((WIDTH,HEIGHT))

clock= pygame.time.Clock()

bg_img= pygame.image.load('Assets\Background\BG1.png')
bg= pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
i = 0



player_idlle =  [pygame.image.load(os.path.join("Assets\Characters\Hero\Black\Idlle", "Black_Idle1.png")),
         pygame.image.load(os.path.join("Assets\Characters\Hero\Black\Idlle", "Black_Idle2.png")),
         pygame.image.load(os.path.join("Assets\Characters\Hero\Black\Idlle", "Black_Idle3.png")),
         pygame.image.load(os.path.join("Assets\Characters\Hero\Black\Idlle", "Black_Idle4.png")),
         pygame.image.load(os.path.join("Assets\Characters\Hero\Black\Idlle", "Black_Idle5.png")),]
       

player_left = [None]*7
for picIndex in range(1,7):
    player_left[picIndex-1] = pygame.image.load(os.path.join("Assets\Characters\Hero\Black\Running", "Black_Run_L" + str(picIndex) + ".png"))
    picIndex+=1

player_right = [None]*7
for picIndex in range(1,7):
    player_right[picIndex-1] = pygame.image.load(os.path.join("Assets\Characters\Hero\Black\Running", "Black_Run_R" + str(picIndex) + ".png"))
    picIndex+=1

zombieMale_left =[pygame.image.load(os.path.join("Assets\Characters\Zombies\male\Walk", "WalkR (1).png")),
         pygame.image.load(os.path.join("Assets\Characters\Zombies\male\Walk", "WalkR (2).png")),
        pygame.image.load(os.path.join("Assets\Characters\Zombies\male\Walk", "WalkR (3).png")),
        pygame.image.load(os.path.join("Assets\Characters\Zombies\male\Walk", "WalkR (4).png")),
        pygame.image.load(os.path.join("Assets\Characters\Zombies\male\Walk", "WalkR (5).png")),
        pygame.image.load(os.path.join("Assets\Characters\Zombies\male\Walk", "WalkR (6).png")),
        pygame.image.load(os.path.join("Assets\Characters\Zombies\male\Walk", "WalkR (7).png")),
        pygame.image.load(os.path.join("Assets\Characters\Zombies\male\Walk", "WalkR (8).png")),
        pygame.image.load(os.path.join("Assets\Characters\Zombies\male\Walk", "WalkR (9).png")),
        pygame.image.load(os.path.join("Assets\Characters\Zombies\male\Walk", "WalkR (10).png")),]

zombieMale_right = [None]*11
for picIndex in range(1,11):
    zombieMale_right[picIndex-1] = pygame.image.load(os.path.join("Assets\Characters\Zombies\male\Walk", "WalkL (" + str(picIndex) + ").png"))
    picIndex+=1



bullet_img = pygame.transform.scale(pygame.image.load(os.path.join("Assets\Objects", "Bullet.png")), (20, 20))


class Hero:
    def __init__(self, x, y):
        #walk
        self.x = x
        self.y = y
        self.velx = 3
        self.vely = 15
        self.face_right = True
        self.face_left = False
        self.idlle = True
        self.stepIndex = 0
        self.idlleIndex = 0
        #jump
        self.jump = False
        #bullet
        self.bullets = []
        self.cool_down_count = 0
        #health
        self.hitbox = (self.x, self.y, 64, 64)
        self.health = 40
        self.lives = 1
        self.alive = True

    def move_hero(self, userInput):
        if userInput [pygame.K_RIGHT] and self.x < 925:
            self.x += self.velx
            self.face_right = True
            self.face_left = False
            self.idlle = False
        elif userInput [pygame.K_LEFT] and self.x > 10:
            self.x -= self.velx
            self.face_right = False
            self.face_left = True
            self.idlle = False
        else :
            self.stepIndex = 0
            self.face_left = False
            self.face_right = False
            self.idlle = True
            
    def draw(self, win):
        self.hitbox = (self.x+ 30, self.y+ 15, 45, 70)
        
        pygame.draw.rect(win, (255,0,0), (self.x+ 30, self.y-5, 40,15))
        if self.health >= 0:
            pygame.draw.rect(win, (0,250,0), (self.x+ 30, self.y-5, self.health,15))

        if self.stepIndex >= 24:
         self.stepIndex = 0

        if self.idlleIndex >= 25:
            self.idlleIndex = 0

        if self.face_left:
            win.blit(player_left[self.stepIndex//4], (self.x, self.y))
            self.stepIndex += 1
        elif self.face_right:
            win.blit(player_right[self.stepIndex//4], (self.x, self.y))
            self.stepIndex += 1
        else :
            win.blit(player_idlle[self.idlleIndex//5], (self.x, self.y))  
            self.idlleIndex += 1     

    def jump_motion(self, userInput):
     if userInput[pygame.K_UP] and self.jump is False:
            self.jump = True
     if self.jump:
            self.y -= self.vely
            self.vely -= 1
     if self.vely < -15:
            self.jump = False
            self.vely = 15

    def direction(self):
        if self.face_right or self.idlle :
            return 1
        if self.face_left :
            return -1

    def cooldown(self):
        if self.cool_down_count >= 20:
            self.cool_down_count = 0
        elif self.cool_down_count > 0:
            self.cool_down_count += 1
        
    def shoot(self):
        self.hit()
        self.cooldown()

        if (userInput[pygame.K_SPACE] and self.cool_down_count == 0):
            bullet = Bullet(self.x, self.y, self.direction())
            self.bullets.append(bullet)
            self.cool_down_count = 1
        for bullet in self.bullets:
            bullet.move()
            if bullet.off_screen():
                self.bullets.remove(bullet)

    def hit(self):
        for enemy in enemies:
            for bullet in self.bullets:
                if enemy.hitbox[0] < bullet.x < enemy.hitbox[0] + enemy.hitbox[2] and enemy.hitbox[1] < bullet.y < enemy.hitbox[1] + enemy.hitbox[3]:
                    enemy.health -= 5
                    player.bullets.remove(bullet)
                    if enemy.health == 0 :
                        enemy.x = 900
                        enemy.health = 40
    

class Bullet:
    def __init__(self, x, y, direction) :
        self.x = x + 63
        self.y = y + 33
        self.direction = direction

    def draw_bullet(self):
        win.blit(bullet_img, (self.x, self.y))
    
    def move(self):
        if self.direction == 1:
            self.x += 15
        if self.direction == -1:
            self.x -= 15
    
    def off_screen(self):
        return not(self.x >= 0 and self.x <= WIDTH)


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stepIndex = 0
        #health
        self.hitbox = (self.x+ 25, self.y+ 15, 45, 70)
        self.health = 40

    def step(self):
        if self.stepIndex >= 40:
            self.stepIndex = 0

    def draw(self, win):
        self.hitbox = (self.x+ 27, self.y+ 15, 40, 80)
        pygame.draw.rect(win, (255,0,0), (self.x+ 20, self.y-5, 40,15))
        if self.health >= 0:
            pygame.draw.rect(win, (0,250,0), (self.x+ 20, self.y-5, self.health,15))
        self.step()
        win.blit(zombieMale_left[self.stepIndex//4], (self.x, self.y))
        self.stepIndex += 1
    
    def move(self):
        self.hit()
        self.x -= 3

    def hit(self):
        if player.hitbox[0] < enemy.x + 32 < player.hitbox[0] + player.hitbox[2] and player.hitbox[1] < enemy.y + 32 <player.hitbox[1] + player.hitbox[3]:
            if player.health > 0:
                player.health -= 1
                if player.health == 0 and player.lives > 0:
                    player.lives -=1
                    player.health =40
                elif player.health == 0 and player.lives == 0 :
                    player.alive = False

           

            

    def off_screen(self):
        return not(self.x >= -50 and self.x <= WIDTH + 50)
    
        


def draw_game():
    win.fill((0, 0, 0))
    # draw looping background
    win.blit(bg, (i,0))
    win.blit(bg, (WIDTH+i, 0))
    # draw enemy
    for enemy in enemies:
        enemy.draw(win)
    # draw bullet
    for bullet in player.bullets:
        bullet.draw_bullet()
    # draw player
    player.draw(win)
    # player health
    if player.alive == False:
        win.fill((255,255,255))
        font = pygame.font.Font("freesansbold.ttf", 32)
        text= font.render("you died press R to restart", True, (0,0,0))
        textrect= text.get_rect()
        textrect.center = (WIDTH//2 ,HEIGHT//2)
        win.blit(text,(textrect))
    if userInput[pygame.K_r]:
        player.alive =True
        player.lives = 1
        player.health = 40

    font = pygame.font.Font("freesansbold.ttf", 32)
    text= font.render("lives: " +str(player.lives), True, (0,0,0))
    win.blit(text, (650,20))
    # frames per second and update
    clock.tick(FPS)
    pygame.display.update()

player = Hero(0 , 380)

enemies = []

run= True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    

    userInput = pygame.key.get_pressed()
    
    if i == -1000:
        win.blit(bg, (WIDTH+i, 0))
        i = 0
    i -= 1

    #shoot
    player.shoot()

    # Movement
    player.move_hero(userInput)
    player.jump_motion(userInput)

    if len(enemies) == 0:
         enemy = Enemy(850, 373)
         enemies.append(enemy)
    for enemy in enemies:
        enemy.move()
        if enemy.off_screen():
            enemies.remove(enemy)


    draw_game()