import pygame as pg
vec = pg.math.Vector2


# sets the values for screen size and frames per second
WIDTH = 1280
HEIGHT = 1024
FPS = 30
#define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SKYBLUE = (135, 206, 235)
GREY = (211, 211, 211)
OFFGREY = (230, 230, 230)
YELLOW = (255, 255, 0)
DARKGREEN = (0, 100, 0)
AMBER = (213, 150, 10)
MAROON = (128, 0 , 0)


#sets variable called title as goose gunner
title = "Goose Gunner"
#sets the amount of pixels per tile
tilesize = 16
#sets the amount of horizontal tiles
tilewidth = WIDTH / tilesize
#sets the amount of vertical tiles
tileheight = HEIGHT / tilesize
#creates a variable called cloud and stores the PNG name in it
cloud = 'cloud.png'
#variable for the background image
background = 'background.png'
#variable for the background video
skyvid = 'skyvid.mpg'

#sets the speed of the player in pixel per frame
playerspeed = 350
#sets the speed of the plane rotation
rotationspeed = 300
#creates a variable called redplane and stores the PNG name in it
redplane = 'redplane.png'
#defines the hit box rectangle
plane_hitrect = pg.Rect(0, 0, 72, 72)
#sets amount for the planes health
plane_health = 100
#sets the knockback for the plane
plane_knockback = 50

#creates a variable called goose and stores the PNG name in it
goose_image = 'goose.png'
#sets the speed of the goose in pixels per frame
goose_speed = [250, 250, 240, 260]
#sets the constant size for the hitrect of the goose
goose_hitrect = pg.Rect(0, 0, 72, 72)
#sets the health of the goose
goose_health = 100
#sets the amount of damage for the geese
goose_damage = 10
#sets the distance for which geese have to avoid each other
goose_radius = 100
#sets the distance geese can detect the plane from
goose_detection = 700

#sets the background music
bg_music = 'rotv.mp3'
#sets a list of goose moans
goose_moans = ['goose_1.mp3', 'goose_2.mp3']
#sets noise when goose dies
goose_death = ['goose_dead.mp3']







#gives a variable ame to the bullet image
bullet_image = 'bullet.png'
#sets speed of the bullet
bullet_speed = 500
#sets lifespan of the bullet in milliseconds
bullet_life = 1500
#sets amount of damage per bullet
bullet_damage = 10
#how fast bullet can shoot when button held down
bullet_rate = 150
#the offset for the bullets on the left wing
gun_offset_l = vec(-20, -29)
#the offset for the bullets on the right wing
gun_offset_r = vec(20, -29)


#sets blood effects
BLOOD_SPLATS = ['bloodsplat_1.png', 'bloodsplat_2.png', 'bloodsplat_3.png', 'bloodsplat_4.png']
#sets the duration of the blood on screen
blood_duration = 1800

#sets the name of the file for high scores
hs_file = "highscore.txt" 

