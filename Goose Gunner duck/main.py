#module imports
import random
import sys
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
        #calls the load data method
        self.loaddata()
        #sets the first round
        self.round = 1
        

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
        #sets the score equal to zero
        self.score = 0    
        #as standard sets pause to false
        self.paused = False
        #runs the run fuction
        self.run()

    
        







    #method for drawing text
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        #sets font
        font = pg.font.Font(font_name, size)
        #renders the surface
        text_surface = font.render(text, True, color)
        #sets the rectangle
        text_rect = text_surface.get_rect()
        #sets positions for differant parts of the rect
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        #draws the image to screen
        self.screen.blit(text_surface, text_rect)

    #game loop
    def run(self):
        #variable that will decide if the game is being played
        self.playing = True
        #plays the music
        pg.mixer.music.play(loops = -1)
        #while loop that ses the running variable
        while self.playing:
            #sets each update to the fps
            self.dt = self.clock.tick(FPS) / 1000
            #runs the events function
            self.events()
            self.draw
            #checks if paused
            if not self.paused:
                print ("hello")
                #runs the update function
                self.update()
            #runs the draw function
                

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
            #plays goose sound
            choice(self.goose_moan_sounds).play()
        #calls the new geeese method
        self.newgeese()
        
    #method for new geese
    def newgeese(self):
        #finds the amount of geese left
        goose_num = len(self.geese)
        #checks if all geese are dead
        if goose_num <= 0:
            #increases the round number
            self.round = self.round + 1
            #repeats for the amount of times as the round
            for x in range(self.round):
                #spawns goose
                goose(self, randint(1, 79), randint(1, 63))
        

             

    #function for loading in files
    def loaddata(self):
        #finds folder that goose gunner is stored in
        self.ggfolder = path.dirname(__file__)
        #creates a list called skymap_data
        self.skymap_data = []
        #opens the gg folder and reads skymp text file
        with open(path.join(self.ggfolder, 'skymap.txt'), 'rt') as f:
            #reads each line
            for line in f:   
                #adds each line from map file to the list
                self.skymap_data.append(line)
        #locates the images folder and stores it as imgfolder
        imgfolder = path.join(self.ggfolder, 'images')
        #locates the sound folder and stores it as sndfolder
        music_folder = path.join(self.ggfolder, 'music')
        #locates music folder and saves it as music_folder
        snd_folder = path.join(self.ggfolder, 'snd')
        
        #find the pause font and loads it
        self.pause_font = path.join(imgfolder, 'Demonized.TTF')
        #sets a translucent layer
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        #sets the level of translucency
        self.dim_screen.fill((0, 0, 0, 200))
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
        #loads in background image
        self.background_image = pg.image.load(path.join(imgfolder, 'background.png')).convert_alpha()
        #creates a list for the blood splates
        self.blood = []
        #in the list in variables named blood splats
        for images in BLOOD_SPLATS:
            #adds images to the blood splats list from the image folder
            self.blood.append(pg.image.load(path.join(imgfolder, images)).convert_alpha())
        #loads the music
        pg.mixer.music.load(path.join(music_folder, bg_music))
        #loads goose moaninging sounds in list
        self.goose_moan_sounds = []
        #goes throught goose moan sounds 
        for snd in goose_moans:
            #appends to the list
            self.goose_moan_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        #creates goose death sounds list
        self.goose_death_sounds = []
        #goes through goose death sounds 
        for snd in goose_death:
            #appends to the list
            self.goose_death_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))

        #opens the high score file
        with open(path.join(self.ggfolder, 'hs_file'), 'a') as h:
            #if there is something in the file already
            try:
                #reads the high score
                self.highscore = int(h.read())
            #if not
            except:
                #sets high score to zero
                self.highscore = 0

        

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
            #checks if a key has been pressed
            if event.type == pg.KEYUP:
                #checks if a esc has been pressed
                if event.key == pg.K_ESCAPE:
                    #toggles pause
                    self.paused = not self.paused

            


    #game loop draw
    def draw(self):
        #draw and render
        self.screen.blit(self.background_image, (0, 0))
        #recognise the individual sprites
        for sprite in self.allsprites:
            #checks if sprite is goose
            if isinstance(sprite, goose):
                #calls the draw health method
                sprite.draw_health()

        #uses the draw plane function to draw the health bar
        draw_plane_health(self.screen, 490, 950, self.plane.health / plane_health)
        #draws sprites
        self.allsprites.draw(self.screen)
        #draws the amount of geese on screen
        self.draw_text('Geese Left: {}'.format(len(self.geese)), self.pause_font, 30,  OFFGREY, 20, 20, align="nw")
        #draws the amount point amount on screen
        self.draw_text("Score: " + str(self.score), self.pause_font, 30, OFFGREY, WIDTH - 20, 20, align="ne")
        #checks if paused
        if self.paused:
            #draws translucent layer
            self.screen.blit(self.dim_screen, (0, 0))
            #draws the paused text
            self.draw_text("Paused", self.pause_font, 100, BLUE, WIDTH / 2, HEIGHT / 2, align="w")
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
        #fills the screen black
        self.screen.fill(BLACK)
        #drwas the text to the screen
        self.draw_text("Geese Gunner", self.pause_font, 100, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
        #draws text to screen
        self.draw_text("Press \"P\" To Play", self.pause_font, 20, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        #draws text to screen
        self.draw_text("High Score: " + str(self.highscore), self.pause_font, 20, WHITE, WIDTH / 2, HEIGHT * 7 / 8, align="center")
        #draws text to the screen
        self.draw_text("SPACE to shoot!", self.pause_font, 20, WHITE, 20, 20, align="w")
        #draws text to the screen
        self.draw_text("A or LEFT to rotate anticlockwise", self.pause_font, 20, WHITE, 20, 50, align="w")
        #draws text to the screen
        self.draw_text("D or RIGHT to rotate clockwise", self.pause_font, 20, WHITE, 20, 80, align="w")
        #flips the display
        pg.display.flip()
        #waits for key to be pressed
        self.wait_for_key()
    
    #method for the game over screen
    def show_dead_screen(self):
        #fills the screen black
        self.screen.fill(BLACK)
        #drwas the text to the screen
        self.draw_text("The Geese Won", self.pause_font, 100, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
        #draws text to screen
        self.draw_text("Press \"P\" To Restart", self.pause_font, 20, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        #checks for new high score
        if self.score > self.highscore:
            #sets new high score
            self.highscore = self.score
            #draws text to screen
            self.draw_text("New High Score: " + str(self.highscore), self.pause_font, 20, WHITE, WIDTH / 2, HEIGHT * 7 / 8, align="center")
            #opens high score file for writing
            with open(path.join(self.ggfolder, 'hs_file'), 'w') as h:
                #writes new high score to file
                h.write(str(self.score))
        else:
            self.draw_text("Geese Lost In Action: " + str(self.score), self.pause_font, 20, WHITE, WIDTH / 2, HEIGHT * 7 / 8, align="center")
        #flips the display
        pg.display.flip()
        #waits for key to be pressed
        self.wait_for_key()

    #method for waiting for a key to be pressed
    def wait_for_key(self):
        #sets waiting to be true
        waiting = True
        #while it is waiting it does the following
        while waiting:
            #ticks the clock so that nothing happens
            self.clock.tick(FPS)
            #checks for an event
            for event in pg.event.get():
                #if the event is quiting
                if event.type == pg.QUIT:
                    #stops the loop
                    waiting = False
                    #stops the game from running
                    self.running = False
                #checks if any button has been pressed
                if event.type == pg.KEYUP:
                    #checks if key is p
                    if event.key == pg.K_p:
                        #stops the loop
                        waiting = False
                    

        


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
    #runs the game
    game.run()
    #shows game over screen
    game.show_dead_screen()
    

pg.quit













 

