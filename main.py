import pygame
from pygame import mixer
from fighter import Fighter
pygame.init()
mixer.init()
SCREEN_WIDTH=1000
SCREEN_HEIGHT=600
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Street Fighter")

#set framerate
clock=pygame.time.Clock()
FPS=60
#define color
YELLOW=(255,255,0)
RED=(255,0,0)
WHITE=(255,255,255)

#define game variables
intro_count=3
last_count_update=pygame.time.get_ticks()
score=[0,0]#player score[p1,p2]
round_over=False
ROUND_OVER_COOLDOWN=2000
#define fighter variables
WARRIOR_SIZE=162
WARRIOR_SCALE=4
WARROR_OFFSET=[72,56]
WARRIOR_DATA=[WARRIOR_SIZE,WARRIOR_SCALE,WARROR_OFFSET]
WIZARD_SIZE=250
WIZARD_SCALE=3
WIZARD_OFFSET=[112,107]
WIZARD_DATA=[WIZARD_SIZE,WIZARD_SCALE,WIZARD_OFFSET]
run=True

#laod music and sound
pygame.mixer.music.load("audio\\music.mp3")
pygame.mixer.music.set_volume(0.5)
sword_fx=pygame.mixer.Sound("audio\sword.mp3")
sword_fx.set_volume(0.5)
magic_fx=pygame.mixer.Sound("audio\magic.wav")
magic_fx.set_volume(0.75)
pygame.mixer.music.play(-1,0.0,500)
#load background image
bg_image=pygame.image.load("Bg_image.jpg").convert_alpha()
#load spritesheets
warrrior_sheet=pygame.image.load("images\warrior\Sprites\warrior.png").convert_alpha()
wizard_sheet=pygame.image.load("images\wizard\Sprites\wizard.png").convert_alpha()
#load victory image
victory_img=pygame.image.load("images\\icons\\victory.png").convert_alpha()

#define number of steps in each animation
WARRIOR_ANIMATION_STEPS=[10,8,1,7,7,3,7]
WIZARD_ANIMATION_STEPS=[8,8,1,8,8,3,7]

#define font
count_font=font = pygame.font.Font(None, 300)
score_font=font = pygame.font.Font(None, 30)

#function for drawing text
def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    screen.blit(img,(x-80,y))


#function for drawing background
def draw_bg():
    scaled_bg=pygame.transform.scale(bg_image,(SCREEN_WIDTH,SCREEN_HEIGHT))
    screen.blit(scaled_bg,(0,0))
def draw_health_bar(health,x,y):
    ratio=health/100
    pygame.draw.rect(screen,WHITE,(x-4,y-4,408,38))
    pygame.draw.rect(screen,RED,(x,y,400,30))
    pygame.draw.rect(screen,YELLOW,(x,y,400*ratio,30))    

#create two instances of fighters
fighter_1=Fighter(1,200,310,False,WARRIOR_DATA,warrrior_sheet,WARRIOR_ANIMATION_STEPS,sword_fx)
fighter_2=Fighter(2,700,310,True,WIZARD_DATA,wizard_sheet,WIZARD_ANIMATION_STEPS,magic_fx)

#game loop
run=True
while run:
    clock.tick(FPS)
    #draw background
    draw_bg()
    

    #show player stats
    draw_health_bar(fighter_1.health,20,20)
    draw_health_bar(fighter_2.health,580,20)
    draw_text("P1:"+str(score[0]),score_font,RED,100,60)
    draw_text("P2:"+str(score[1]),score_font,RED,660,60)
    #update countdown
    if intro_count<=0:
         #move fighters
         fighter_1.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen,fighter_2,round_over)
         fighter_2.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen,fighter_1,round_over) 
    else:
        #display count timer
        draw_text(str(intro_count),count_font,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/3)
        #update count timer
        if(pygame.time.get_ticks()-last_count_update)>=1000:
            intro_count-=1
            last_count_update=pygame.time.get_ticks()
            print(intro_count)
   
    # fighter_2.move()

    #update fighters
    fighter_1.update()
    fighter_2.update()

    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)
   
    #check for player defeat
    if round_over==False:
        if fighter_1.alive==False:
            score[1]+=1
            round_over=True
            round_over_time=pygame.time.get_ticks()
        elif fighter_2.alive==False:
            score[0        ]+=1
            round_over=True
            round_over_time=pygame.time.get_ticks() 
    else:
        #display victory image
        screen.blit(victory_img,(350,150))
        if pygame.time.get_ticks()-round_over_time>ROUND_OVER_COOLDOWN:
            round_over=False
            intro_count=3
            fighter_1=Fighter(1,200,310,False,WARRIOR_DATA,warrrior_sheet,WARRIOR_ANIMATION_STEPS,sword_fx)
            fighter_2=Fighter(2,700,310,True,WIZARD_DATA,wizard_sheet,WIZARD_ANIMATION_STEPS,magic_fx)
  

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    #update display
    pygame.display.update()      
#exit pygame
pygame.quit()            


