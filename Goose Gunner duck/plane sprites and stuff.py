


#sets up plane sprite class
class Plane(pygame.sprite.Sprite):
    #sprite for the plane
    def __init__(self):
        #initialises itself
        pygame.sprite.Sprite.__init__(self)

        #loads in image for my player entity
        self.load = pygame.image.load(os.path.join(imgfolder,"blueplane.png")).convert()
        self.image = self.load
        self.image.set_colorkey(WHITE)

        #uses a rectangle for the entity
        self.rect = self.image.get_rect()
        #tells the entity where to start
        self.rect.center = (WIDTH/2, HEIGHT/2)


    #is going to use the sprite group to update
    def update(self):
        #every update the entity moves right 5 pixels
        self.rect.x += 1
        #checks to see if the entity has gone off screen
        if self.rect.left > WIDTH:
            #moves entity to the left hand side of screen
            self.rect.right = 0













#uses the plane class and stores it as plane
plane = Plane()
#uses that entity and adds it to the game
allsprites.add(plane)




#sets up the asset folders
#finds where the game file is stored
game_folder = os.path.dirname(__file__)
#connects game folder to the image folder
imgfolder = os.path.join(game_folder, "images")