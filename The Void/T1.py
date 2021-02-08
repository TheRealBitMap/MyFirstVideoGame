import pygame
from pygame import *
import time
import random
pygame.init()

clock = pygame.time.Clock()

black = (255,255,255)
white = pygame.image.load('bg.jpg')
#menu = pygame.image.load('bg3.jpg')
menu = pygame.image.load('bg1.jpg')
red = (255,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

music = pygame.mixer.music.load('the_final_battle.ogg')
pygame.mixer.music.play(-1)

bg = pygame.image.load('bg.jpg')
 
#SCREEN_SIZE = pygame.Rect((0, 0, 800, 600)) #this is for defining screen size

TILE_SIZE = 32 # character size and grey tiles
GRAVITY = pygame.Vector2((0, 0.3)) #2d vector
display_width = 800
display_height = 600
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
SCREEN_SIZE = pygame.display.set_mode((display_width,display_height))

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(SCREEN_SIZE, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(SCREEN_SIZE, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("TextPixal",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    SCREEN_SIZE.blit(textSurf, textRect)


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #SCREEN_SIZE.fill(white)
        #SCREEN_SIZE.blit(white,(0,0))
        SCREEN_SIZE.blit(menu, (0,0))
        pygame.init()
        largeText = pygame.font.SysFont("TextPixal",115)
        TextSurf, TextRect = text_objects("THE VOID", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        SCREEN_SIZE.blit(TextSurf, TextRect)

        button("PLAY!",150,450,100,50,green,bright_green,main)
        button("Quit :(",550,450,100,50,red,bright_red,pygame.quit)

        pygame.display.update()
        clock.tick(15)

        
class CameraAwareLayeredUpdates(pygame.sprite.LayeredUpdates):
    # This defines the world size and creates a target for cam to follow
    def __init__(self, target, world_size):
        super().__init__()
        self.target = target
        self.cam = pygame.Vector2(0, 0)
        self.world_size = world_size
        if self.target:
            self.add(target)

    #This defines what the target is
    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + display_width/2
            y = -self.target.rect.center[1] + display_height/2
            self.cam += (pygame.Vector2((x, y)) - self.cam) * 0.05
            self.cam.x = max(-(self.world_size.width-display_width), min(0, self.cam.x))
            self.cam.y = max(-(self.world_size.height-display_height), min(0, self.cam.y))

    #This defines the cam to follow the target
    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        init_rect = self._init_rect
        for spr in self.sprites():
            rec = spritedict[spr]
            newrect = surface_blit(spr.image, spr.rect.move(self.cam))
            if rec is init_rect:
                dirty_append(newrect)
            else:
                if newrect.colliderect(rec):
                    dirty_append(newrect.union(rec))
                else:
                    dirty_append(newrect)
                    dirty_append(rec)
            spritedict[spr] = newrect
        return dirty

def redrawGameWindow():
    SCREEN_SIZE.blit(bg, (0,0))

#This defines the level to play in and the genaral info, such as title
def main():
    pygame.init()
    screen = pygame.display.set_mode([display_width,display_height])
    pygame.display.set_caption("THE VOID")
    timer = pygame.time.Clock()
    pygame.mixer.music.stop()
    music = pygame.mixer.music.load('dungeon_theme.ogg')
    pygame.mixer.music.play(-1)
    

    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P                    PPPPPPPPPPP           P",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P    PPPPPPPP                              P",
        "P                                          P",
        "P                          PPPPPPP         P",
        "P                 PPPPPP                   P",
        "P                                          P",
        "P         PPPPPPP                          P",
        "P                                          P",
        "P                     PPPPPP               P",
        "P                                          P",
        "P   PPPPPPPPPPP                            P",
        "P                                          P",
        "P                 PPPPPPPPPPP              P",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]


    platforms = pygame.sprite.Group()
    player = Player(platforms, (TILE_SIZE, TILE_SIZE))
    level_width  = len(level[0])*TILE_SIZE
    level_height = len(level)*TILE_SIZE
    entities = CameraAwareLayeredUpdates(player, pygame.Rect(0, 0, level_width, level_height))

    # build the level
    x = y = 0
    for row in level:
        for col in row:
            if col == "P":
                Platform((x, y), platforms, entities)
            if col == "E":
                ExitBlock((x, y), platforms, entities)
            x += TILE_SIZE
        y += TILE_SIZE
        x = 0

    while 1:

        for e in pygame.event.get():
            if e.type == QUIT: 
                return
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                return

        entities.update()

        #screen.fill((0, 0, 0))
        screen.blit(white,(0,0))
        entities.draw(screen)
        pygame.display.update()
        timer.tick(60)

class EntityDiff(pygame.sprite.Sprite):
    def __init__(self, color, pos, *groups):
        super().__init__(*groups)
        self.image = Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        #self.image = pygame.image.load('brick (1).png')
        self.rect = self.image.get_rect(topleft=pos)
        
#This defines what the sprite looks like
class Entity(pygame.sprite.Sprite):
    def __init__(self, color, pos, *groups):
        super().__init__(*groups)
        #self.image = Surface((TILE_SIZE, TILE_SIZE))
        self.image = pygame.image.load('standing.png')
        #self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)


        
#This defines the sprites attrabutes and gives it speed and jump streingth
class Player(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(Color("#0000FF"), pos)       
        self.vel = pygame.Vector2((0, 0))
        self.onGround = False
        self.platforms = platforms
        self.speed = 8
        self.jump_strength = 13

    #this defines colliding, jumping and moving the char
    def update(self):
        pressed = pygame.key.get_pressed()
        up = pressed[K_UP]
        left = pressed[K_LEFT]
        right = pressed[K_RIGHT]
        running = pressed[K_SPACE]

        if right:
            #self.image = walkRight
            self.image = pygame.image.load('R1.png')
        if left:
            #self.image = walkLeft
            self.image = pygame.image.load('L1.png')

        if up:
            if self.onGround: self.vel.y = -self.jump_strength
        if left:
            self.vel.x = -self.speed
        if right:
            self.vel.x = self.speed
        if running:
            self.vel.x *= 1.5
        if not self.onGround:
            self.vel += GRAVITY
            if self.vel.y > 100: self.vel.y = 100
        print(self.vel.y)
        if not(left or right):
            self.vel.x = 0
        self.rect.left += self.vel.x
        self.collide(self.vel.x, 0, self.platforms)
        self.rect.top += self.vel.y
        self.onGround = False;
        self.collide(0, self.vel.y, self.platforms)


    #this gives the output from the arrow keys (moving the actual char)
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom

class Platform(EntityDiff):
    def __init__(self, pos, *groups):
        super().__init__(Color("#9400D3"), pos, *groups)
        self.image = pygame.image.load('brick (1).png')

class ExitBlock(Platform):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)
        

if __name__ == "__main__":
    
    game_intro()
    main()

#game_intro()
pygame.quit()
quit()
