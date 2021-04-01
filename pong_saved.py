#Final project CS 150 fall 2014
#a one player game of pong
#pong.py
#using pygame
#pygame Techniques learned from Paul Vincent Craven of Simpson college's website
#http://programarcadegames.com/
#Kenneth Allen






import pygame ## the library that supplies graphics and keyboard input features
import time
import random 

black    = (   0,   0,   0)   #tuples that represent rgb color codes
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
purple   = ( 166, 140, 173)
orange   = ( 255, 165,   0)
blue     = (   0,   0, 255)
 
list_of_colors = [orange,green,red,purple,blue,black,black] 
pygame.init()

width = 800    # width and height of the screen 
height = 500  # just the height of the playing area not the health bar

### lower barrier ####
bottom = 30  # the part of the screen where the health bar is

size = (width, height+bottom)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")
 
done = False
 
clock = pygame.time.Clock() #controls the frames per second of the game

name = "name"

##############CONTROLS###############

screen_color = white

#PUCK
radius = 10
puck_start_x = width/2
puck_start_y = height/2
puck_dx = 7
puck_dy = 0
move_up = False
move_down = False
acceleration = 0

# BORDER
border_width = 5

#Player Paddle########
player_height = 100
player_start_x = 40
player_start_y = height/2 - player_height/2
player_width = 5

###computer paddle####
computer_height = 100
computer_start_x = width - 40
computer_start_y = height/2 - player_height/2
computer_speed = 1
computer_width = 5

###TOTAL HEALTH##
start_health = 3


###NEW GAME INCREMENTS###
computer_speed_change = 3
puck_speed_change = 3


#####################################

player_y_positions = []
computer_y_positions = []

pygame.mouse.set_visible(False) #hides the mouse in the game




def plus_or_minus(n):
    x = random.randint(0,1)
    if x == 1:
        return -1*n
    else:
        return n

class Game(object): #class that organizes methodes that run a particular game
    
    
    def __init__(self,name):
        self.name = name
        
    def computer_score(self): #determins if the puck pased the player's side of the screen
        if the_puck.x < -50*abs(the_puck.dx):  #the -50 gives a bit of extra time for the ball to reset and start play again
            #print "computer score"
            player.health -= 1
            self.reset_puck_pos()
            
    def player_score(self): #determins if the puck pased the computer's side of the screen
        if the_puck.x > width+50*abs(the_puck.dx):  #the +50 gives a bit of extra time for the ball to reset and start play again
            #print "player score"
            computer.health -= 1
            self.reset_puck_pos()

    
    def reset_puck_pos(self): #puts the puck back in the center after a goal
        temp_puck_dx = the_puck.dx
        the_puck.dx = 0
        the_puck.dy = 0
        the_puck.x = puck_start_x
        the_puck.y = puck_start_y
        self.reset_puck_speed(temp_puck_dx)
        
    def reset_puck_speed(self,puck_speed): # gives the puck speed after a goal
        the_puck.dx = plus_or_minus(puck_speed)
        the_puck.dy = random.randint(-1,1)
    
    def display_lose(self): #shoes a big L when you loose
        for i in range(100):
            if i < 50:
                pygame.draw.line(screen,red,(50+width/3,3*height/4),(50+width/3+4*i,3*height/4),20)
                pygame.draw.line(screen,red,(50+width/3,3*height/4),(50+width/3,3*height/4-7*i),20)
            pygame.display.flip()
            clock.tick(60)
        
    def display_win(self): #shows a big W when you loose
        for i in range(100):
            if i < 50:
                pygame.draw.line(screen,green,(100+width/6,height/4),(100+width/6,height/4+4*i),5)
                pygame.draw.line(screen,green,(100+width/6,height/4+4*50),(100+width/6+4*i,height/4+50*4-4*i),20)
                pygame.draw.line(screen,green,(100+width/6+50*4,height/4),(100+width/6+50*4,height/4+4*i),5)
                pygame.draw.line(screen,green,(100+width/6+4*50,height/4+4*50),(100+width/6+4*50+4*i,height/4+50*4-4*i),20)

                
                
            pygame.display.flip()
            clock.tick(60)

    
    def restore_constants(self): #resets variables that are chagned in the fun stuff class
        player.height = player_height
        computer.height = computer_height
        the_puck.radius = radius
        screen_color = white

class Puck(object): #class that controls the motion of the puck
   
    def __init__(self,color,x,y,radius,dx,dy):
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = dx
        self.dy = dy

    def draw(self): #redraws the puck in each frame
        pygame.draw.circle(screen,self.color,[int(self.x),int(self.y)],self.radius,0)
        
    def move_x(self):  #changes the puck x and y positions each turn by their "speed" dx and dy
        self.x += self.dx
        self.y += self.dy
        
        
    def bounce(self): #chagnes the pucks direction when the puck reaches a paddle or a wall
        if self.y > height-self.radius-border_width:
            self.dy  = -abs(self.dy)  #using abs() instead of *-1 makes prevents bug where the ball can get stuck to the wall
        if self.y < self.radius+border_width:
            self.dy = abs(self.dy)
        if self.x < player.x + self.radius+3 and self.x >=player.x-5 and self.y>player.Yrange()[0] and self.y<player.Yrange()[1]:
            self.dx = abs(self.dx) # y range represents the y  values where a paddle is
            self.dy += player.get_speed(player_y_positions)/4
        if self.x > computer.x - self.radius-3 and self.x <=computer.x+5 and self.y>computer.Yrange()[0] and self.y<computer.Yrange()[1]:
            self.dx = -abs(self.dx)
            self.dy += computer.get_speed(computer_y_positions)/10
            
    def ghost_draw(self): # this methode draws a puck in the middle of the screen after a goalso that that player knows that the game is about to start
        #this puck has not speed and dispears when the game starts
        if the_puck.x > width+25*abs(the_puck.dx) or the_puck.x < -25*abs(the_puck.dx):
            pygame.draw.circle(screen,self.color,[puck_start_x,puck_start_y],self.radius,0)
    
    def change_color(self,screen_color): #changes the color of the puck so that it goes with the screen background
        if screen_color == red:
            self.color = green
        if screen_color == blue:
            self.color = red
        if screen_color == green:
            self.color = red
        if screen_color == white:
            self.color = black
        if screen_color  == black:
            self.color = white
    
        
class Paddle(object): #superclass with general methodes that both the computer's and player's paddle needs
    
    def __init__(self,x,y,width,height,color):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.colo = color
        
    
    def Yrange(self): #returns that y values that are covered by the puck at any given time so the puck knows when to bounce
        return (self.y-the_puck.radius,self.y+self.height+the_puck.radius)
    
    def draw(self): #redraws the paddle in eacj frame
        pygame.draw.line(screen,self.color,(self.x,self.y),(self.x,self.y+self.height),self.width)
        
    def y_pos_list(self,L): #creates a list if the last 2  positions of a paddle for the next methode
        L.append(self.y)
        if len(L) > 2:
            L.pop(0)

        
    def get_speed(self,L): #returns the diffence between the last two y coordinates so get the paddle speed
        if len(L) > 1:
            speed = L[1] - L[0]
            return speed
        
    def change_color(self,screen_color): #changes the color of the paddle just for fun
        if screen_color == red:
            self.color = green
        if screen_color == blue:
            self.color = red
        if screen_color == green:
            self.color = red
        if screen_color == white:
            self.color = black
        if screen_color  == black:
            self.color = white
    
        
    

class Player(Paddle): #subclass of Paddle to controle the user's paddle
    
    health = start_health
    
    def __init__(self,x,y,width,height,color):
        Paddle.__init__(self,x,y,width,height,color)
    
    def update_pos(self,mouse_y):  #redraws the paddle so that he middle of the paddle is at the y position of the mouse
        self.y = mouse_y - self.height/2
    
    
class Computer(Paddle): #controls the computer paddle (subclass of Paddle)
    
    health = start_health
    
    def __init__(self,x,y,width,height,color,speed):
        Paddle.__init__(self,x,y,width,height,color)
        self.speed = speed
        
        #the computer paddles only reacts when the ball crosses the half way line
        #I determined that it looks more human this way
        #it then follows that ball's y postition at it;s max speed which is controlled in the constants above
        #if the paddle can reach the ball at less the top speed it does this to prevent it from jittering back and
        #forth at top speed
            
    def move(self):
        if abs(self.y+self.height/2-the_puck.y) < self.speed:
            self.dx = abs(self.y+self.height/2-the_puck.y)
        else:
            self.dx = self.speed
            
        if the_puck.x > (width/2) and the_puck.x < width and the_puck.dx > 0:
            if self.y+self.height/2 > the_puck.y and self.y> 0:
                self.y -= self.dx
            if self.y+self.height/2 < the_puck.y and self.y+self.height < height:
                self.y += self.dx
                
        else:
            if self.y+self.height/2 > height/2:
                self.y -= self.dx/2
            if self.y+self.height/2 < height/2:
                self.y += self.dx/2

            
class Fun_stuff(object): #a few methodes that happen at random when you press space
    
    fun_stuff_count = 3 # the number of fun things that one can do, each win gives you another
    
    def player_paddle(self): #makes the player paddle larger or smaller
        x = random.randint(0,1)
        if x == 1:
            player.height = player_height*2
        if x == 0:
            player.height = player_height/2
            
    def computer_paddle(self): #makes the computer paddle larger or smaller
        x = random.randint(0,1)
        if x == 1:
            computer.height = computer_height*2
        if x == 0:
            computer.height = computer_height/2
            
    def ball_size(self): #change the size of the ball between two random values
        x = random.randint(1,50)
        the_puck.radius = x
        
            
    
    def do_fun_stuff(self): #decides which fun_stuff methode to randomly select when space is pushed
        x = random.randint(0,3)
        if x == 0:
            self.player_paddle()
        if x == 1:
            self.computer_paddle()
        if x == 2:
            self.ball_size()
        if x > 2:
            new_screen_color = random.choice(list_of_colors)
            return new_screen_color
            
        
    
        
    
    
fun = Fun_stuff()  #instaces of each class created with parameters controlled in constance way above
game = Game(name)
the_puck = Puck(black,puck_start_x,puck_start_y,radius,puck_dx,puck_dy)
player = Player(player_start_x,player_start_y,player_width,player_height,black)
computer = Computer(computer_start_x,computer_start_y,computer_width,computer_height,computer_speed,white)

def play(player_wins,comp_wins,comp_speed = computer_speed, puck_speed = puck_dx,level = 0,screen_color = white):
    #function like main() that controls plays 1 game with the parameters entered above
    the_puck.dx = puck_speed
    computer.speed = comp_speed
    
    
    done = False #the basic loop structure as learned from simpson college pygame tutorial
    while not done: #ends the game when exit buttom is clicked on loops until then
        # --- Main event loop
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                done = True
            elif event.type == pygame.KEYDOWN:  #controls if a key is pressed 
                if event.key == pygame.K_SPACE and fun.fun_stuff_count >0:
                    fun.fun_stuff_count -= 1
                    
                    new_color = fun.do_fun_stuff()
                    
                    if type(new_color) == tuple: #chagnes the color of the screen based on a radom choice from a list of colors
                        screen_color = new_color
                        
        mouse_pos = pygame.mouse.get_pos() # return the mouse position
        mouse_y = mouse_pos[1]  #takes the y part of the mouse pos tuple
        if mouse_y < player.height/2:  # prevents a paddle from exeeding the edge of the screen
            mouse_y = player.height/2
        if mouse_y > height-player.height/2:
            mouse_y = height-player.height/2
    
        

        #PUCK #########     
        the_puck.move_x()
        the_puck.bounce()
        the_puck.change_color(screen_color)
        ######
        
        ###PLAYER METHODES####   
        player.update_pos(mouse_y)
        player.y_pos_list(player_y_positions)
        player.change_color(screen_color)
        
        
        ####COMPUTER METHODES####
        computer.move()
        computer.y_pos_list(computer_y_positions)
        computer.change_color(screen_color)
    
        ####THE GAME METHODES#####
        game.computer_score()
        game.player_score()
        
        ########################
        screen.fill(screen_color) #fills the screen with this color each frame for animation
        #everything is redraws in the new position dictated by the drawring methodes below
    
        ####graphics ####
        
        ######RINK GRPHICS######## draws lines on the screen such as the borders and the center line and circle
        if screen_color == red: 
            pygame.draw.line(screen,blue,(width/2,0),(width/2,height),2)
        else:
            pygame.draw.line(screen,red,(width/2,0),(width/2,height),2)
        pygame.draw.circle(screen,black,(width/2,height/2),100,2)
    
        pygame.draw.rect(screen,black,[0,0,width,border_width],0)
        pygame.draw.rect(screen,black,[0,height-border_width,width,height],0)
        
        #####HEALTH BAR GRAPHICS#######
        pygame.draw.line(screen,white,(5,height+bottom/2),((player.health*width)/10,height+(bottom)/2),5)
        pygame.draw.line(screen,white,(width-5,height+bottom/2),(width-(computer.health*width)/10,height+(bottom)/2),5)
        
    
        #########################
        
        #####PUCK METHODES##### draws the puck at it's update position
        the_puck.draw()
        the_puck.ghost_draw() #placeholder puck for when one scores

        #######################
        #####PLAYER/COMPUTER DRAE#####
        player.draw()
        computer.draw()
        
        #####################
        #both the player and computer atart of with a set number of lives
        #when those run out the following code runs
        
        #once you click close this part of the code runs and produces a laundry list of error messages
        #ro prevent this from happening I used exeption handling
        #this is useful becasue the commandline return feedback on how your win/loss record
        
        try:
            if player.health < 0: #aka player loses
                game.display_lose()  #shows a big "L"
                print "you: ",player_wins,"computer: ",comp_wins+1,"level: ",level-1 #prints the numer of wins and loses and the level
                player.health = start_health #resets yours and the computer health to max
                computer.health = start_health
                game.restore_constants() #restores constances chaged with fun_stuff
                fun.fun_stuff_count += 1 #gives you and extra fun stuff point
                
                comp_new_speed = comp_speed - computer_speed_change  #sets the speed for the next game
                if comp_new_speed < 1:       # if you loose the computer and puck go slower
                    comp_new_speed = 1
                puck_new_speed = puck_speed-puck_speed_change
                if puck_new_speed < 3:
                    puck_new_speed = 3
                    
    #the play function is called recursivley to start a new game with changed paramters based on whether you won or lost the last one
                
                play(player_wins,comp_wins+1,comp_new_speed,puck_new_speed,level-1) 
            if computer.health < 0: #same thing for if you win the game speed up this time though
                fun.fun_stuff_count += 1
                game.display_win()
                print "you: ",player_wins+1,"computer: ",comp_wins,"level: ",level+1
                player.health = start_health
                computer.health = start_health
                game.restore_constants()
                
                play(player_wins+1,comp_wins,comp_speed + computer_speed_change,puck_speed+puck_speed_change,level+1)
        
            pygame.display.flip()  #pygame methode that updates the screen with all of the new features
        except Exception:
            pass
     
        
     
        clock.tick(60)
     
    pygame.quit() #quits the game when the loops is exited but clicking close
    
try:
    play(0,0)
except Exception:
    print "have a nice day!!!"  #when you click exit an error is produced
    #the exeption prevents error messages and prints have a nice day instead