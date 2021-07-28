import pygame 
import os
import random
import math

from pygame.constants import KEYDOWN, K_LEFT, K_RIGHT, K_UP
from pygame import mixer 

pygame.font.init()
pygame.mixer.init()

width, height= 900,500
blue= (25,200,220)
fps=50                 #sets the game to a constant 60 fps 
speed=5                 #speed of the vacccine 
max_persmissible_bullet=5       # max persmissible bullet on the screen
number_of_enemies=6
c_speed=1
bullet_state="not fired"        # by defeault bullet  is not fired
bullet_speed=6
score_val=0

score_x=10
score_y=10
game_over_x, game_over_y=50,100

font=pygame.font.Font('Risalah Cinta.otf',30)

finish_font=pygame.font.Font('Risalah Cinta.otf', 60)

corona_width,corona_height= 100, 100
vaccine_width, vaccine_height=100, 100
bullet_width, bullet_height=20, 20
bullet_x,bullet_y= 0,400
 
#for multiple enemies



#surfaces
background=pygame.image.load(os.path.join("corona blaster","hospital3.jpg"))        
#corona_image=pygame.image.load(os.path.join("corona blaster","coro.png"))  
vaccine_image=pygame.image.load(os.path.join("corona blaster","vaccine1.png"))
bullet_image=pygame.image.load(os.path.join("corona blaster","drop.png"))
Game_finish_image=pygame.image.load(os.path.join("corona blaster","game_over.jpg"))
  
#corona=pygame.transform.scale(corona_image,(corona_width, corona_height))
vaccine=pygame.transform.scale(vaccine_image,(vaccine_width, vaccine_height))
bullet=pygame.transform.rotate(pygame.transform.scale(bullet_image,(bullet_width, bullet_height)),180)
bg=pygame.transform.scale(background,(width,height))
Game_finish=pygame.transform.scale(Game_finish_image,(width,height))

window= pygame.display.set_mode((width,height))
pygame.display.set_caption("CORONA BLASTER ")

#setting up the enemy positions for respawing 

#corona_x=random.randint(0,width)
#corona_y=random.randint(40,height/2)


corona=[]
corona_speed=[]
corona_x=[]
corona_y=[]

def displayScore(x,y):
    score =font.render("Score: " + str(score_val)+"                                                                                STAY AT HOME ", True,(255,255,255))
    window.blit(score,(x,y))
 
 
 
for i in range(number_of_enemies):
   corona_image=pygame.image.load(os.path.join("corona blaster","coro.png"))              
   corona.append(pygame.transform.scale(corona_image,(corona_width, corona_height)))
   
   corona_x.append(random.randint(0,width))
   corona_y.append(random.randint(40,height/2))
   corona_speed.append(c_speed)
   
def gameOver():
       window.blit(Game_finish,(0,0))
       over=finish_font.render(" CORONA INVADED !! GAME OVER!! " ,True, (255,255,255))
       window.blit(over,(game_over_x,game_over_y))
   
def corona_movement():
    #global corona_x, corona_y,corona_speed
    for i in range(number_of_enemies):
        
        if(corona_y[i]>500):
            for i in range(number_of_enemies):
                corona_y[i]=1000
            gameOver()
            break
            
        
        corona_x[i]+=corona_speed[i] 
        if(corona_x[i] >=width-50):
            corona_speed[i] =-corona_speed[i]
            corona_y[i]+=abs(corona_speed[i])+50
        elif(corona_x[i]<=0):
            corona_speed[i]=abs(corona_speed[i])
            corona_y[i]+=abs(corona_speed[i])+50
    
  
def fire_bullet(b_x,b_y):
    global bullet_state
    bullet_state='fire'
    window.blit(bullet,((b_x+30),b_y-10))
    pygame.display.update()
    
def iscolliding(corona_x,corona_y,bullet_x,bullet_y):                       #for checking collision
    
    distance= math.sqrt(pow(corona_x-bullet_x,2)+pow(corona_y-bullet_y,2))
    if(distance<40):
        return True
    else:      
        return False
    
def draw_window(vacc_pos):              #for drawing window
     
    window.blit(bg,(0,0))
    for i in range(number_of_enemies):
        window.blit(corona[i],(corona_x[i],corona_y[i]))
        corona_movement()    
    window.blit(vaccine,(vacc_pos.x,vacc_pos.y))
    
    #pygame.display.update()
   # for bullets in vacc_bullet:
    #    pygame.draw.rect(window)
     #   window.blit(bullet,(bullets.x,bullets.y))
         
    

def main():                 # main function
    global bullet_y,bullet_state,score_val,bullet_x
    
    vacc_bullet=[]
    vacc_pos=pygame.Rect(450,400,vaccine_width, vaccine_height)
    clock=pygame.time.Clock()   
    run=True
    while(run):
        clock.tick(fps)         #to set the fps 
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                run=False
        keys_pressed=pygame.key.get_pressed()           # gives the set of all the keys that are pressed 
        
            # for movement 
        if keys_pressed[K_LEFT] and vacc_pos.x>0:                    #left button 
            vacc_pos.x-=speed                       #vaccine shifts to left side
            
        if keys_pressed[K_RIGHT] and vacc_pos.x <width-100:                   #right button 
            vacc_pos.x+=speed
            
            #bullet
        if event.type== KEYDOWN:
            if event.key==K_UP :                         #fire bullets 
               # bullet=pygame.Rect(vacc_pos.x+ vaccine_width/2,vacc_pos.y+vaccine_height, bullet_width,bullet_height )
                #vacc_bullet.append(bullet)
                if bullet_state=="not fired":
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()              
                    bullet_x=vacc_pos.x
                    fire_bullet(bullet_x, bullet_y)
        
        if(bullet_y<=0):
            bullet_y=400
            bullet_state="not fired"
        if bullet_state=="fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y-=bullet_speed
        
                            
        draw_window(vacc_pos)
        
        for i in range(number_of_enemies):
            if(iscolliding(corona_x[i],corona_y[i],bullet_x,bullet_y)):
                explosion_sound=mixer.Sound('explosion.wav')
                explosion_sound.play()
                bullet_y=400                                        #reset the bullet     
                bullet_state="not fired"
                score_val+=1
                corona_x[i]=random.randint(0,width)
                corona_y[i]=random.randint(40,height/2)
                print(score_val)
        displayScore(score_x,score_y)
        pygame.display.update()    
    pygame.quit()
    
    

    
if __name__=='__main__':
    main()
    