import pygame
from pygame.locals import*
import random
import sys
import os
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
pygame.init()
pygame.mixer.init()
clock=pygame.time.Clock()
fps=60
screen_width=720
screen_height=780
screen=pygame.display.set_mode((screen_width,screen_height))
game_surface = pygame.Surface((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')
font =pygame.font.SysFont('Bauhaus 93', 60)
white=(255,255,255)
ground_scroll=0
scroll_speed=4
flying=False
game_over=False
pipe_gap=150
pipe_freq=1500
last_pipe=pygame.time.get_ticks() - pipe_freq
score=0
pass_pipe=False
muted = False
fullscreen=False

bg=pygame.image.load(resource_path('img/bg.png'))
ground_img=pygame.image.load(resource_path('img/ground.png'))
wing_fx = pygame.mixer.Sound(resource_path("sounds/wing.mp3"))
point_fx = pygame.mixer.Sound(resource_path("sounds/point.mp3"))
die_fx = pygame.mixer.Sound(resource_path("sounds/die.mp3"))
print(resource_path("sounds/wing.mp3"))
print(os.path.exists(resource_path("sounds/wing.mp3")))
button_image=pygame.image.load(resource_path('img/restart.png'))
sound_on=pygame.image.load(resource_path("img/volume_on.png"))
sound_off=pygame.image.load(resource_path("img/volume_off.png"))
sound_on = pygame.transform.scale(sound_on, (50, 50))
sound_off = pygame.transform.scale(sound_off, (50, 50))
fullscreen_on = pygame.image.load(resource_path("img/fullscreen_on.png"))
fullscreen_off = pygame.image.load(resource_path("img/fullscreen_off.png"))
fullscreen_on = pygame.transform.scale(fullscreen_on, (50,50))
fullscreen_off = pygame.transform.scale(fullscreen_off, (50,50))
exit_button_image = pygame.image.load(resource_path('img/exit.png'))
exit_button_image = pygame.transform.scale(exit_button_image, (50, 50))

pygame.mixer.music.load(resource_path("sounds/music.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    game_surface.blit(img, (x,y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x=100
    flappy.rect.y=int(screen_height/2)
    score=0
    return score

def toggle_fullscreen():
    global screen, fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen_width, screen_height))

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for num in range(1, 4):
            img = pygame.image.load(resource_path(f"img/bird{num}.png"))
            self.images.append(img)
        self.image=self.images[self.index ]
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.vel=0
        self.clicked=False

    def update(self):
        if flying:
            self.vel+=0.5
            if self.vel>8:
                self.vel=8
            if self.rect.bottom<768:
                self.rect.y += int(self.vel)

        if not game_over:
            keys = pygame.key.get_pressed()
            if (pygame.mouse.get_pressed()[0] or keys[pygame.K_SPACE]) and not self.clicked:
                self.clicked = True
                self.vel = -10
                wing_fx.play()
            if not pygame.mouse.get_pressed()[0] and not keys[pygame.K_SPACE]:
                self.clicked = False
            self.counter +=1
            flap_cooldown=5
            if self.counter>flap_cooldown:
                self.counter=0
                self.index+=1
                if self.index >=len(self.images):
                    self.index=0
            self.image=pygame.transform.rotate(self.images[self.index],self.vel*-2)
        else:
            self.image=pygame.transform.rotate(self.images[self.index],-90)

class pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(resource_path('img/pipe.png'))
        self.rect=self.image.get_rect()
        if position ==1:
            self.image= pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft=[x,y - int(pipe_gap/2)]
        if position==-1:
            self.rect.topleft=[x,y + int(pipe_gap/2)]
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right<0:
            self.kill()

class Button():
    def __init__(self,x,y, image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.clicked=False
    def draw(self):
        action=False
        mx, my = pygame.mouse.get_pos() 
        if fullscreen:
            mx = mx * screen_width / screen.get_width()
            my = my * screen_height / screen.get_height()
        pos = (mx, my)
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and not self.clicked:
                action=True
                self.clicked=True
        if pygame.mouse.get_pressed()[0]==0:
            self.clicked=False

        game_surface.blit(self.image,(self.rect.x,self.rect.y))
        return action

bird_group=pygame.sprite.Group()
pipe_group=pygame.sprite.Group()
flappy=Bird(100,int(screen_height/2))
bird_group.add(flappy)

button=Button(screen_width//2-50, screen_height//2-100,button_image)
mute_button=Button(screen_width - 60,10,sound_on)
fullscreen_button=Button(screen_width -120,10,fullscreen_off)
exit_button = Button(10, 10, exit_button_image)

run=True
while run:
    clock.tick(fps)
    game_surface.blit(bg,(0,0))
    bird_group.draw(game_surface)
    bird_group.update()
    pipe_group.draw(game_surface)
    

    game_surface.blit(ground_img,(ground_scroll,768))

    if len(pipe_group)>0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.left < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe=True
        if pass_pipe==True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score +=1
                point_fx.play()
                pass_pipe= False

    draw_text(str(score), font, white, int(screen_width/2), 20)

    if (pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0) and not game_over:
        game_over=True
        pygame.mixer.music.stop()
        die_fx.play()

    if flappy.rect.bottom >= 768 and not game_over:
        game_over=True
        flying=False
        pygame.mixer.music.stop()
        die_fx.play()
    if game_over == False and flying ==True:
        time_now=pygame.time.get_ticks()
        if time_now - last_pipe > pipe_freq:
            pipe_height=random.randint(-100,100)
            btm_pipe=pipe(screen_width,int(screen_height/2) + pipe_height,-1)
            top_pipe=pipe(screen_width,int(screen_height/2) + pipe_height,1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe=time_now

        ground_scroll-=scroll_speed
        if abs(ground_scroll)>35:
            ground_scroll=0
        pipe_group.update()

    if game_over:
       if button.draw():
           game_over=False
           score= reset_game()
           pygame.mixer.music.play(-1)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if (event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)) \
            and not flying and not game_over:
            flying = True

    if muted:
        mute_button.image=sound_off
    else:
        mute_button.image=sound_on
    if mute_button.draw():
        muted=not muted
        if muted:
            pygame.mixer.music.set_volume(0)
        else:
                pygame.mixer.music.set_volume(0.5)

    if fullscreen:
        fullscreen_button.image = fullscreen_off   # أيقونة الخروج من الفول سكرين
    else:
        fullscreen_button.image = fullscreen_on    # أيقونة الدخول للفول سكرين

    if fullscreen_button.draw():
        toggle_fullscreen()
    if exit_button.draw():
        run = False

    if fullscreen:
        scaled = pygame.transform.scale(
            game_surface,
            (screen.get_width(), screen.get_height())
        )
        screen.blit(scaled, (0, 0))
    else:
        screen.blit(game_surface, (0, 0))
    pygame.display.update()
pygame.quit()
