import pygame,math,random

screen_width = 800
screen_height = 600

Colour_Black = 0,0,0 # -> will screen fill
Colour_Green = 144,206,57 

# Game properties:
Text_Padding = 25 # control how far the score of player is displayed on edge of screen
Paddle_Speed = 5   # will control speed of paddle up and down when input key is hit
Paddle_Offset =10  # spacing paddle off the screen
Ball_Speed = 3
Spin_Percent = 0.5 # represent motion of ball when hit paddle -> Ball will pick up half of the momentum of paddle

# Classes:
class vector2: #? This class evokes co-ordinates to be used as vectors.
    def __init__(self,X = 0,Y = 0):
        self.x = X
        self.y = Y
    def __add__(self,other):
        if isinstance(other,vector2): # isinstance checks if other is a vector
            return vector2(self.x + other.x, self.y + other.y) 
        else:
            return vector2(self.x + other, self.y + other) # will return scalar vector 
        
    def __Mul__(self,other):
        if isinstance(other,vector2,): # isinstance checks if other is a vector
            return vector2(self.x * other.x, self.y * other.x) 
        else: 
            return vector2(self.x * other, self.y * other)
        
        
    def set_to_Zero(self):
        self.x = 0
        self.y = 0 

class Actor: #? Evokes where the ball and player will be placed and their speed
    def __init__(self,Texture):
        # Below variables are going to be used to use pos and vel to move object for the actor
        self.position = vector2() 
        self.velocity = vector2()
        self.texture = Texture # Surface reference

    def Get_Bounds(self): # Used to make a rectangle in which the actor occupies to move around
        return pygame.Rect(self.position.x, self.position.y, self.texture.get_rect().width, self.texture.get_rect().height)
    
    def Move(self, amounttomove):
        self.position += amounttomove 
    
    def center_y(self):
        self.position.y = screen_height / 2 - self.texture.get_rect().height / 2

    def center_xy(self):
        self.position = vector2(screen_width / 2 - self.texture.get_rect().width / 2,
                                screen_height / 2 - self.texture.get_rect().height / 2)

 
class Ball(Actor): # Inheriting syntax 
    #? This ball is an actor which in this class you spawn it, depending on position and give it speed
    def Move(self,amounttomove):
        Actor.Move(self,amounttomove)
        global Plyer1score,Plyer2score #? by making them global we are giving them recognition to be used within this class

        if self.position.y < 0: # Top of scree
            self.velocity.y = math.fabs(self.velocity.y)
        elif self.position.y > screen_height - self.Get_Bounds().height: # Below of screen 
            self.velocity.y = -math.fabs(self.velocity.y)

        if self.Get_Bounds().right < 0:
            Player2.score += 1
            Plyer2score = TheFont.render("%d" % Player2.score, 1, Colour_Green)
            self.Launch(Ball_Speed)
        elif self.position.x > screen_width:
            Player1.score += 1
            Plyer1score = TheFont.render("%d" % Player2.score, 1, Colour_Green)
            self.Launch(Ball_Speed)
        
    def Launch(self, speed):
        self.center_xy()
        var = random.uniform(-1,1) # will get a random floating point between -1 and 1
        Angle = math.pi / 2 + var # Math.pi gives half a circle, which then divided by 2 gives quater of circle 
        if random.randint(0,1) == 0: # Go to left direction
            Angle += math.pi
        
        self.velocity.x = math.sin(Angle)
        self.velocity.y = math.cos(Angle)
        
        self.velocity = self.velocity.__Mul__(speed)            
            
class Player(Actor):
    score = 0

    def Move(self, amounttomove):
        Actor.Move(self, amounttomove)

        if self.position.y < 0:
            self.position.y = 0   
        elif self.position.y > screen_height - self.texture.get_rect().height:
            self.position.y =  screen_height - self.texture.get_rect().height 


#Initialisation:
pygame.init() # Initialises pygame
screen = pygame.display.set_mode((screen_width,screen_height))
 

#Textures:
BallTexture = pygame.image.load(r"C:\Users\munav\OneDrive\Documents\Documents\learning python\Pythonprogramming.py\Beginners\ball.png")
PlayerTexture = pygame.image.load(r"C:\Users\munav\OneDrive\Documents\Documents\learning python\Pythonprogramming.py\Beginners\bat.png")

TheFont = pygame.font.Font(None,100) #? Font for the score
Plyer1score = TheFont.render("0",1, Colour_Green)
Plyer2score = TheFont.render("0",1, Colour_Green)


#GameObjects:
ball = Ball(BallTexture)
ball.Launch(Ball_Speed)

Player1 = Player(PlayerTexture)
Player1.position.x = Paddle_Offset
Player1.center_y()

Player2 = Player(PlayerTexture)
Player2.position.x = screen_width - Player2.Get_Bounds().width - Paddle_Offset
Player2.center_y()


#Functions:
def Update(elapsedtime): #? Will evoke changes to the game -> will move the ball, player depending on the changes
    timefactor = elapsedtime * 0.05
    Player1.velocity.set_to_Zero() #! This is needed to make sure the we don't have to keep pressing the keys for movement ensuring hold
    Player2.velocity.set_to_Zero()
    Keys = pygame.key.get_pressed()
    if Keys[pygame.K_w]:
        Player1.velocity.y -= Paddle_Speed
    if Keys[pygame.K_s]:
        Player1.velocity.y += Paddle_Speed
    if Keys[pygame.K_UP]:
        Player2.velocity.y -= Paddle_Speed
    if Keys[pygame.K_DOWN]:
        Player2.velocity.y += Paddle_Speed


    ball.Move(ball.velocity.__Mul__(timefactor)) # Will always now go at right pace watever the processors speed might be
    Player1.Move(Player1.velocity.__Mul__(timefactor))
    Player2.Move(Player2.velocity.__Mul__(timefactor))

    if pygame.Rect.colliderect(ball.Get_Bounds(), Player1.Get_Bounds()): #? check if collided
        ball.velocity.x = math.fabs(ball.velocity.x)
        ball.velocity.y = ball.velocity.y.__add__(Player1.velocity.y).__mul__(Spin_Percent)
    elif pygame.Rect.colliderect(ball.Get_Bounds(),Player2.Get_Bounds()):
        ball.velocity.x = -math.fabs(ball.velocity.x)
        ball.velocity.y = ball.velocity.y.__add__(Player2.velocity.y).__mul__(Spin_Percent) 

    

def Draw(): #? Is responsible for the envoking the texture using the blit method 
    screen.fill(Colour_Black)
    screen.blit(ball.texture,ball.Get_Bounds())
    screen.blit(Player1.texture,Player1.Get_Bounds())
    screen.blit(Player2.texture,Player2.Get_Bounds())

    screen.blit(Plyer1score, (Text_Padding,Text_Padding))
    screen.blit(Plyer2score, (screen_width - Plyer2score.get_width() - Text_Padding, Text_Padding))
    pygame.display.flip()   

# Loop control and timing -> Tracking time per update 
GameOver = False
lastTick = pygame.time.get_ticks() 
elapsedtime = 0

#Gameloop
while not GameOver: 
    events = pygame.event.get() # all events in a list
    for event in events:
        if event.type == pygame.QUIT:
            GameOver = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            GameOver = True 
    
    elapsedtime = pygame.time.get_ticks() - lastTick #! Will keep the game consistent depending on the processors speed.
    lastTick = pygame.time.get_ticks()

    Update(elapsedtime) # Update will occur based on the elapsed time
    Draw() # State of game is drawn to screen

