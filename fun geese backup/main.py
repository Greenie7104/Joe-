#module imports
import random
from os import path
import pygame as pg
from variables import *
from sprites import *




class game:

    #initialises the game window (when game object is created)
    def __init__(self):
        #initialises pygame
        pg.init()
        #initialises the sound
        pg.mixer.init()
        #takes the set width and height and creates window to match
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        #adds caption to the top of the window
        pg.display.set_caption(title)
        #computes how many milliseconds have past since the previous call
        self.clock = pg.time.Clock()
        #allows the movement to move when holding down the button (milliseconds)
        pg.key.set_repeat(100, 100)
        #sets running to true
        self.running = True
        self.loaddata()

    #starts a new game
    def new(self):
        #controls all pygame sprites
        self.allsprites = pg.sprite.Group()
        #creates walls group instance
        self.walls = pg.sprite.Group()
        #creates goose group instance 
        self.geese = pg.sprite.Group()
        #creates bullets group instance
        self.bullets = pg.sprite.Group()
        #gives the name and place of any given thing in the file33
        for row, tiles in enumerate(self.skymap_data):
            #does the same for each colunm
            for col, tile in enumerate(tiles):
                #checks for wall
                if tile == '1':
                    #if true creates wall where the 1 is
                    wall(self, col, row)
                #checks for goose
                if tile == 'g':
                    #if true creates wall where the g is
                    goose(self, col, row)
                #checks if tile is p
                if tile =='p':
                    #spawns player
                    self.plane = plane(self, col, row)
        #runs the run fuction
        self.run()

        

    #game loop
    def run(self):
        #variable that will decide if the game is being played
        self.playing = True
        #while loop that ses the running variable
        while self.playing:
            #sets each update to the fps
            self.dt = self.clock.tick(FPS) / 1000
            #runs the events function
            self.events()
            #runs the update function
            self.update()
            #runs the draw function
            self.draw()

    #game loop updates
    def update(self):
        #updates the sprite group
        self.allsprites.update()
        #uses group collide function to to define what is going to be hit
        hits = pg.sprite.spritecollide(self.plane, self.geese, False, collidehitrect)
        #when it hits
        for hit in hits:
            #akes away the amount of damage the goose has inflicted
            self.plane.health -= goose_damage
            #slows down the plane
            hit.vel = vec(0, 0)
            #checks if the player health is less than zero
            if self.plane.health <= 0:
                #if true sets the playing to false
                self.playing = False
        #checks if hit
        if hits:
            #knocks the sprite back
            self.plane.pos += vec(plane_knockback, 0).rotate(-hits[0].rot)
        #uses group collide function to to define what is going to be hit
        hits = pg.sprite.groupcollide(self.geese, self.bullets, False, True)
        #when it hits
        for hit in hits:
            #takes away the bullet damage from the goose
            hit.health -= bullet_damage
            #slows down the goose
            hit.vel = vec(0, 0)

    #function for loading in files
    def loaddata(self):
        #finds folder that goose gunner is stored in
        ggfolder = path.dirname(__file__)
        #creates a list called skymap_data
        self.skymap_data = []
        #opens the gg folder and reads skymp text file
        with open(path.join(ggfolder, 'skymap.txt'), 'rt') as f:
            #reads each line
            for line in f:
                #adds each line from map file to the list
                self.skymap_data.append(line)
        #locates the images folder and stores it as imgfolder
        imgfolder = path.join(ggfolder, 'images')
        #finds the redplane image and stores it as self.plane_image and converts it into the correct pixelsize
        self.plane_image = pg.image.load(path.join(imgfolder, 'redplane.png')).convert_alpha()
        #finds the bullet image and stores it as self.bullet_image and converts it into the correct pixelsize
        self.bullet_image = pg.image.load(path.join(imgfolder, 'bullet.png')).convert_alpha()
        #downscales the image to be suitable for the game
        self.bullet_image = pg.transform.scale(self.bullet_image, (10, 10))
        #finds the goose image and stores it as self.goose_image and converts it into the correct pixelsize
        self.goose_image = pg.image.load(path.join(imgfolder, 'goose.png')).convert_alpha()
        #finds the cloud image and stores it as self.cloud_image and converts it into the correct pixelsize
        self.cloud_image = pg.image.load(path.join(imgfolder, 'cloud.png')).convert_alpha()
        #resizes the cloud image to fit 
        self.cloud_image = pg.transform.scale(self.cloud_image, (tilesize, tilesize))
        

    #game loop events
    def events(self):
        #checks for events
        for event in pg.event.get():
            #checks if event is quiting the window
            if event.type == pg.QUIT:
                #checks if playing is true
                if self.playing:
                    #if so sets playing to false
                    self.playing = False
                #sets running to falsed
                self.running = False

            


    #game loop draw
    def draw(self):
        #draw and render
        self.screen.fill(SKYBLUE)
        #recognise the individual sprites
        for sprite in self.allsprites:
            #checks if sprite is goose
            if isinstance(sprite, goose):
                #calls the draw health method
                sprite.draw_health()

        #uses the draw plane function to draw the health bar
        draw_plane_health(self.screen, 490, 950, self.plane.health / plane_health)



        #runs drawgrid function
        #aself.drawgrid()
        #draws sprites
        self.allsprites.draw(self.screen)
        #after drawing display is fliped
        pg.display.flip()



    #draw grid function
    def drawgrid(self):
        #calculates distance between vertical lines and repeats
        for x in range(0, WIDTH, tilesize):
            #draws the line
            pg.draw.line(self.screen, BLACK, (x, 0), (x, HEIGHT))

        #calculates distance between horizontal lines and repeats
        for y in range(0, HEIGHT, tilesize):
            #draws the line
            pg.draw.line(self.screen, BLACK, (0, y), (WIDTH, y))




    #shows start screen
    def show_start_screen(self):
        pass
    
    #game over screen
    def show_dead_screen(self):
        pass


#function for drawing the health bar
def draw_plane_health(surf, x, y, pct):
    #checks if health is less than zero
    if pct < 0:
        #sets percent to zero
        pct = 0
    #sets bar length
    bar_length = 300
    #sets bar height
    bar_height = 50
    #sets how much should be filled
    fill = pct * bar_length
    #sets the outline box 
    outline_rect = pg.Rect(x, y, bar_length, bar_height)
    #sets the filled bar
    fill_rect = pg.Rect(x, y, fill, bar_height)
    #checks if greater than 60 percent
    if pct > 0.6:
        #sets colour to green
        colour = DARKGREEN
    #checks if greater than 30 percent
    elif pct > 0.3:
        #sets colour to zero
        colour = AMBER
    #checks for other percentage
    else:
        #sets colour to red
        colour = MAROON
    #draws the health bar
    pg.draw.rect(surf, colour, fill_rect)
    #draws the outline
    pg.draw.rect(surf, GREY, outline_rect, 3)



#creates instance of game class
game = game()
#will show a start screen
game.show_start_screen()
#controls wether game is running
while game.running:
    #starts new game
    game.new()
    #shows game over screen
    game.show_dead_screen()
    

pg.quit













 

