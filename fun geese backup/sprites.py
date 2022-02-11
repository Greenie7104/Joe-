import pygame as pg
from pygame.constants import GL_CONTEXT_ROBUST_ACCESS_FLAG
from pygame.transform import rotate
from variables import *
from random import choice
#imports vectors from pygame
vec = pg.math.Vector2

#defines the wall collisons
def wallcollide(sprite, group, dir):
    #checks the x dirrection
    if dir == 'x':
        #calls the sprite collide function in variable called collision
        hits = pg.sprite.spritecollide(sprite, group, False, collidehitrect)
        #defines what to do if collision is true
        if hits:
            #checks colision to the right
            if hits[0].rect.centerx > sprite.hitrect.centerx:
                #defines where the sprite should now be
                sprite.pos.x = hits[0].rect.left - sprite.hitrect.width / 2

            #checks collision to the left
            if hits[0].rect.centerx < sprite.hitrect.centerx:
                #defines where the sprite should now be
                sprite.pos.x = hits[0].rect.right + sprite.hitrect.width / 2
            #sets velocity to zero
            sprite.vel.x = 0
            #gives new position
            sprite.hitrect.centerx = sprite.pos.x
    #checks the y dirrection
    if dir == 'y':
        #calls the sprite collide function in variable called collision
        hits = pg.sprite.spritecollide(sprite, group, False, collidehitrect)
        #defines what to do if collision is true
        if hits:
            #checks collision up
            if hits[0].rect.centery > sprite.hitrect.centery:
                #defines where the sprite should now be
                sprite.pos.y = hits[0].rect.top - sprite.hitrect.height / 2

            #checks collision down
            if hits[0].rect.centery < sprite.hitrect.centery:
                #defines where the sprite should now be
                sprite.pos.y = hits[0].rect.bottom + sprite.hitrect.width / 2
            #sets velocity to zero
            sprite.vel.y = 0
            #gives new position
            sprite.hitrect.centery = sprite.pos.y

#sets up plane class 
class plane(pg.sprite.Sprite):
    #initialses class
    def __init__(self, game, x, y):
        #creates sprite group called s_group
        self.s_group = game.allsprites
        #creates base class using s_group
        pg.sprite.Sprite.__init__(self, self.s_group)
        #allows game to be used by the plane class
        self.game = game
        #sets tile to the plane image
        self.image = game.plane_image
        #creates a box for the sprite
        self.rect = self.image.get_rect()
        #sets the hit rect to the self.hitrect
        self.hitrect = plane_hitrect
        #sets the center of the hitrect
        self.hitrect_center = self.rect.center
        #uses vectors to set the velocities to zero
        self.vel = vec(0,0)
        #sets position vector
        self.pos = vec(x, y) * tilesize
        #keeps track of the sprites dirrection
        self.rot = 0
        #sets last shot to zero
        self.last_shot = 0
        #sets the health attribute to the plane health variable
        self.health = plane_health
        

    #function for the key movements
    def getkeys(self):
        #sets the default rotation speed to 0
        self.rotationspeed = 0

        #uses vectors to set the velocities to zero
        self.vel = vec(0,0)
        
        #variable for if keys are pressed
        keys = pg.key.get_pressed()

        #what to do if key is pressed for left
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            #rotation speed is set
            self.rotationspeed = rotationspeed

        #what to do if key is pressed for right
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            #rotation speed is set
            self.rotationspeed = -rotationspeed

        #forwardmovement not in loop so will be constant
        self.vel = vec(0, -playerspeed).rotate(-self.rot)


        #if space key is pressed
        if keys[pg.K_SPACE]:
            #finds the time passed since last shot
            now = pg.time.get_ticks()
            #checks if time since last shot is greater than the bullet rate
            if now - self.last_shot > bullet_rate:
                #resets time since last shot
                self.last_shot = now
                #sets direction of the bullet
                dir = vec(0, -1).rotate(-self.rot)
                #sets position of the bullet for the left 
                pos_l = self.pos + gun_offset_l.rotate(-self.rot)
                #spawns bullet for the left
                bullet(self.game, pos_l, dir)
                #sets position of the bullet for the right 
                pos_r = self.pos + gun_offset_r.rotate(-self.rot)
                #spawns bullet for the right
                bullet(self.game, pos_r, dir)
                   
       

        
            


    #defines code for updating position
    def update(self):
        #calls on getkeysfunction
        self.getkeys()
        #calculates the player rotation and tracks the reainder so that it wont go over 360
        self.rot = (self.rot + self.rotationspeed * self.game.dt) % 360
        #changes the rotation on screen
        self.image = pg.transform.rotate(self.game.plane_image, self.rot)
        #sets the new rectangle
        self.rect = self.image.get_rect()
        #sets the position of the new center of the rectangle
        self.rect.center = self.pos
        #calculates position using velocities
        self.pos += self.vel * self.game.dt
        #sets rectangle x to the new x
        self.hitrect.centerx = self.pos.x
        #calls wallcolide funtion in x dirrection
        wallcollide(self, self.game.walls, 'x')
        #sets rectangle y to the new y
        self.hitrect.centery = self.pos.y
        #calls wallcolide funtion in y dirrection
        wallcollide(self, self.game.walls, 'y')
        #sets the rect centres equal to one another
        self.rect.center = self.hitrect.center
        
        




    

#sets up goose class 
class goose(pg.sprite.Sprite):
    #initiates the class
    def __init__(self, game, x , y):
        #allows game class to be used
        self.game = game
        #makes goose part of alsprites group and goose group
        self.s_group = game.allsprites, game.geese
        #initialises both sprite groups 
        pg.sprite.Sprite.__init__(self, self.s_group)
        #sests the goose image
        self.image = game.goose_image
        #sets the goose rectangle
        self.rect = self.image.get_rect()
        #sets the goose hit rect to the size specified in variables
        self.hitrect = goose_hitrect.copy()
        #sets the centre of the hit rect
        self.hitrect.center = self.rect.center
        #sets goose positiion
        self.pos = vec(x, y) * tilesize
        #sets center of rect
        self.rect.center = self.pos
        #rotation value in degrees for the goose
        self.rot = 0
        #sets rotation attribute
        self.vel = vec(0, 0)
        #sets acceleration attribute
        self.acc = vec(0, 0)
        #sets the health for the geese
        self.health = goose_health
        #sets speed to a random number from the varaible for goose speed
        self.speed = choice(goose_speed)

    #update definiitions fpr the method
    def update(self):
        #calculates the direction of the goose
        self.rot = (self.game.plane.pos - self.pos).angle_to(vec(1,0))
        #rotates the imamge with correspondence to the direction set above
        self.image = pg.transform.rotate(self.game.goose_image, self.rot)
        #sets the rectangle position
        self.rect = self.image.get_rect()
        #sets the centre of the rectangle
        self.rect.center = self.pos
        #updates the goose's acceleration in the correct direction
        self.acc = vec(1, 0).rotate(-self.rot)
        #calls method to find the net vector
        self.avoid_geese()
        #scales the acceleartion to the goose speed
        self.acc.scale_to_length(self.speed)
        #adds negative acceleration 
        self.acc += self.vel * -1 
        #updates the goose's velocity
        self.vel += self.acc * self.game.dt
        #updates the goose's position
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        #sets the centre of the rectangle x coordinates
        self.hitrect.centerx = self.pos.x
        #uses the wallcollide function for x
        wallcollide(self, self.game.walls, 'x')
        #sets the centre of the rectangle y coordinates
        self.hitrect.centery = self.pos.y
        #uses the wallcollide function for y
        wallcollide(self, self.game.walls, 'y')
        #sets the centre of the rectangle
        self.rect.center = self.hitrect.center
        #checks if health is less than or equal to zero
        if self.health <= 0:
            #kills goose
            self.kill()

    #method for the geese to be avoiding one another
    def avoid_geese(self):
        #loops through all geese
        for goose in self.game.geese:
            #not including the goose being targeted
            if goose != self:
                #distance from the goose to another goose
                dist = self.pos - goose.pos
                #checks if length is less than the radius
                if 0 < dist.length() < goose_radius:
                    #adds up the net value 
                    self.acc += dist.normalize()






    #method for drawin the health bar
    def draw_health(self):
        #checks if greater than 60
        if self.health > 60:
            #sets colour to green
            colour = DARKGREEN
        #checks if greater than 30 and less than 60
        elif self.health <= 60 and self.health > 30:
            #sets colour to yellow
            colour = AMBER
        #anything else is
        else:
            #sets colour to red
            colour = MAROON
        #sets a value for the width of the bar
        width = int(self.rect.width * self.health / goose_health)
        #defines the parameters of the health bar
        self.health_bar = pg.Rect(0, 0, width, 8)
        #checks if health is less than 100
        if self.health < goose_health:
            #draws health bar
            pg.draw.rect(self.image, colour, self.health_bar)





#sets up new class called bullet      
class bullet(pg.sprite.Sprite):
    #initiialises the bullet class
    def __init__(self, game, pos, dir):
        #makes the class a part of the allsprites and bullets group
        self.groups = game.allsprites, game.bullets
        #initialises the sprite
        pg.sprite.Sprite.__init__(self, self.groups)
        #sets the bullet image
        self.image = game.bullet_image
        #stores game reference 
        self.game = game
        #sets the bullet rectangle
        self.rect = self.image.get_rect()
        #sets rectangle centre
        self.rect.center = pos
        #sets the position
        self.pos = vec(pos)
        #sets the bullet velocity
        self.vel = dir * bullet_speed
        #tracks time since spawned
        self.spawn_time = pg.time.get_ticks()

    #update method for the bullet class
    def update(self):
        #sets the new bullet positiion
        self.pos +=  self.vel * self.game.dt
        #sets where the new centre is
        self.rect.center = self.pos
        #checks if the bullet has outlasted its lifetime
        if pg.time.get_ticks() - self.spawn_time > bullet_life:
            #bullet ends
            self.kill()





        




#sets up wall class 
class wall(pg.sprite.Sprite):
    #initiates the class
    def __init__(self, game, x , y):
        #makes wall part of alsprites group and walls group
        self.s_group = game.allsprites, game.walls
        #initialises both sprite groups 
        pg.sprite.Sprite.__init__(self, self.s_group)
        #allows game to be used by the plane class
        self.game = game
        #sets size of the wall
        self.image = game.cloud_image
        #defines the rectangle 
        self.rect = self.image.get_rect()
        #defines width of box in pixel coordinates
        self.x = x
        #defines height of box in pixel coordinates
        self.y = y
        #sets the rect to the correct location on the grid
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize

#function that takes both sprites as parameters
def collidehitrect(one, two):
    #returns the colide rectangle compared against the wall rect
    return one.hitrect.colliderect(two.rect)





