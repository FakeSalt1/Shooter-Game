x = 100
y = 100
o = 0
o2 = 1000
from pygame import*
from random import randint, choice
import time as timer


window_width = 1000
window_height = 1000
window = display.set_mode((window_width,window_height))


randint (1,15)
font.init()
style = font.SysFont(None,50)

bg = transform.scale(image.load("galaxy.jpg"),(window_width,window_height))

clock = time.Clock()
fps = 60
game = True
finish = False
isCreateBoss = True

last_fire_rate = timer.time()
fire_rate = 0.2

isReload = False
realod = 2
reload_blink_count = 0
d = 0

mag = 50

class Character(sprite.Sprite):
    def __init__(self,filename,size_x,size_y,pos_x,pos_y, speed,hp):
        super().__init__()
        self.filename = filename
        self.size_x = size_x
        self.size_y = size_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed
        self.image = transform.scale(image.load(self.filename),(self.size_x, self.size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.hp = hp
        self.max_hp = hp
    def draw(self):
        window.blit(self.image, (self.rect.x,self.rect.y))
class UFO(Character):
    def update(self):
        global o

        self.rect.y += self.speed
        if (self.rect.y > window_height):
            self.respawn()
            o+=1
            
            print(o2)
    def respawn(self):
        self.rect.y = 0
        self.rect.x = randint(100,900)
        self.speed = randint(3,5)
        print ("res")
    def isShot(self):
        global d  
        print("ufodie")
        self.hp -=  100
        if self.hp <= 0:
            if self.max_hp : 
                self.respawn()
                d+=1    
                self.hp = self.max_hp
class Bullets(Character):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
class Astroid(Character):
    def __init__(self,filename,size_x,size_y,pos_x,pos_y, speed,hp):
        self.speed_x = speed * choice([1,-1])   
        self.speed_y = speed * choice([1,-1])   
        super().__init__(filename,size_x,size_y,pos_x,pos_y, speed,hp)
    def update(self):
        self.rect.y -= self.speed
        self.rect.x -= self.speed


astroid_group = sprite.Group()
astroid_group.add  (Astroid("whoask.png",randint(500,600),600,50,50,2,1))
astroid_time = timer.time()



player1 = Character("rocket.png",70,140,500,500,5,100)


ufo_group = sprite.Group()
for i in range(5) :
    x = randint (100,900)
    s = randint (1,3)
    ufo_type = choice(["ufo.png","ufo.png"])
    ufo_group.add  (UFO(ufo_type,200,140,x,100,s,100))


bullet_group = sprite.Group()


    




while game:
    display.update()
    clock.tick(fps)

    window.blit(bg,(0,0))
    player1.draw()
    ufo_group.draw(window)
    bullet_group.draw(window)
    

    text = style.render("Pass:" + str(o), True,(255,255,255))
    window.blit(text,(0,100))
    text = style.render("hp:" + str(player1.hp), True,(255,255,255))
    window.blit(text,(0,200))
    text = style.render("mag:" + str(mag), True,(255,255,255))
    window.blit(text,(0,300))
    if d <= 25:
        text = style.render("Quest: Kill All" + str(d) + "/25", True, (225,225,225))
        window.blit(text,(200,100))

    astroid_group.draw(window)
    
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish == False:
        ufo_group.update()
        bullet_group.update()
        astroid_group.update()

        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and player1.rect.y > 0:
            player1.rect.y -= player1.speed
            
        elif keys_pressed[K_d] and player1.rect.x < window_width-player1.size_x:
            player1.rect.x  += player1.speed
            
        elif keys_pressed[K_a] and player1.rect.x >  0:
            player1.rect.x  -= player1.speed
            
        elif keys_pressed[K_s] and player1.rect.y <window_height-player1.size_y:
            player1.rect.y  += player1.speed
            
        elif keys_pressed[K_SPACE] and timer.time() - last_fire_rate > fire_rate and mag > 0:
            bullet_group.add(Bullets("bullet.png",50,50,player1.rect.x,player1.rect.y,10,0))
            last_fire_rate  = timer.time()
            mag -= 1

            print(mag)
            if mag <=  0 :
                print("reload")
                isReload = True
                start_reload = timer.time()

        if isReload == True:
            if timer.time() -  start_reload > realod:
                mag+=50
                isReload = False
            else:
                if reload_blink_count < 20:
                    text_reload = style.render("Reloading",True, (255,255,255))
                elif reload_blink_count < 40:
                    text_reload = style.render("",True, (255,255,255))
                else:
                    reload_blink_count = 0
                reload_blink_count += 1
                window.blit(text_reload,(400,400))

                


        
        collide_list = sprite.spritecollide(player1, ufo_group,False)
        

        for collided_ufo in collide_list:
            collided_ufo.respawn()
            player1.hp -= 20

        collide_dictionary = sprite.groupcollide(bullet_group,ufo_group,True,False)
        for collided_bullet in  collide_dictionary.keys():
            ufo_list = collide_dictionary[collided_bullet]
            hit_ufo = ufo_list[0]
            hit_ufo.isShot()

        if player1.hp <= 0:
            finish = True
        if d == 50:
            
            text_result = style.render("YOU WIN", True, (225,225,225))
            window.blit(text_result,(200,200))
            finish = True
        if d >= 24:
            text = style.render("Quest: Kill All 25/25", True, (225,225,225))
            window.blit(text,(200,100))
            text = style.render("Quest: Kill All 2 "+ str(d) + "/50", True, (225,225,225))
            window.blit(text,(200,200))

        if d == 25:
            text_result = style.render("BOSS INCOMING", True, (225,225,225))
            window.blit(text_result,(500,0))
            if isCreateBoss == True:
                ufo_group.add(UFO("asteroid.png",50,75,x,0,1,1000))
                isCreateBoss = False
        if timer.time() - astroid_time > 2:
            astroid_group.add  (Astroid("whoask.png",randint(500,600),600,50,50,2,1))
            astroid_time = timer.time()
    else:   
    
        if player1.hp <= 0:
            text_result = style.render("YOU LOSE", True, (225,225,225))
        else:
            text_result = style.render("YOU WIN", True, (225,225,225))
        window.blit(text_result,(200,200))



# player2 = Character("cyborg.png",100,100,300,300,5)
# treasure = Character("treasure.png",100,100,900,670,0)
# rocks = Character("rocks.png",200,120,400, 500, 0)


# #w1 = Wall(50,900,200,100)
# #w2 = Wall(50,900,500,-300)
# #w3 = Wall(50,900,900,100)
# wall_list= []
# wall_list.append(Wall(50,900,200,100))
# wall_list.append(Wall(50,900,400,-300))
# wall_list.append(Wall(250,50,550,100))
# wall_list.append(Wall(250,50,450,250))
# wall_list.append(Wall(50,900,800,100))




# route_list = []
# for i in range(6):
#     x = random.randint(0,window_width)
#     y = random.randint(0,window_height)
#     route_list.append((x,y))
# print(route_list)

# route = 0
# ok_x = False
# ok_y =  False

# while game:
#     window.blit(bg,(0,0))
#     for e in event.get():
#         if e.type == QUIT:
#             game = False
#     if finish == False:
#         safety_x = player1.rect.x
#         safety_y = player1.rect.y
#         keys_pressed = key.get_pressed()
#         if keys_pressed[K_w] and player1.rect.y > 0:
#             player1.rect.y -= player1.speed
#         elif keys_pressed[K_d] and player1.rect.x < window_width-player1.size_x:
#             player1.rect.x  += player1.speed
#         elif keys_pressed[K_a] and player1.rect.x >  0:
#             player1.rect.x  -= player1.speed
#         elif keys_pressed[K_s] and player1.rect.y <window_height-player1.size_y:
#             player1.rect.y  += player1.speed
#         for wall in wall_list:
#             isCollide = sprite.collide_rect(player1,wall)
#             if isCollide:
#                 player1.rect.x = safety_x
#                 player1.rect.y = safety_y
        

#         goto_x, goto_y= route_list [route]
#         if (ok_x == False):
#             d = abs(player2.rect.x - goto_x)
#             if (player2.rect.x - goto_x):
#                 player2.rect.x += min(player2.speed, d)
#             elif (player2.rect.x > goto_x): 
#                 player2.rect.x -= min(player2.speed, d)
#                 ok_x = True
#         if (ok_y == False):
#             d = abs(player2.rect.y - goto_y)
#             if (player2.rect.y < goto_y):
#                 player2.rect.y += min(player2.speed, d)
#             elif (player2.rect.y > goto_y): 
#                 player2.rect.y -= min(player2.speed, d)
#             else:
#                 ok_y = True   
#         if (ok_x== True and ok_y == True):
#             route += 1
#             ok_x = False
#             ok_y = False
#             if (route == len(route_list)): 
#                 route = 1
        


        
#         iscollide = sprite.collide_rect(player1,player2)
#         if iscollide:
#             print("YOU WERE HURT BY CYBROG")
#             hp -= 40 
#             player1.rect.x = 50
#             player1.rect.y = 670
#         iscollide = sprite.collide_rect(player1,rocks)
#         if iscollide:
#             hp -= 10            
#             print("YOU WERE HURT BY ROCKS")
#             player1.rect.y = 670
                            
#         iscollide = sprite.collide_rect(player1,treasure)
#         if iscollide:
#             finish = True
#     else:
#         if hp <= 0:
#             text_END = style.render("YOU LOSE", True, (225,225,225))
#         else:
#             text_END = style.render("YOU WIN", True, (225,225,225))
#         window.blit(text_END,(200,200))

#     text_hp = style.render("HP:"+str(hp), True, (225,225,225))
#     window.blit(text_hp,(10,10))
#     player1.show()
#     player2.show()
#     treasure.show()
#     rocks.show()



#     for wall in wall_list:
#         wall.show()
#     display.update()
#     clock.tick(fps)