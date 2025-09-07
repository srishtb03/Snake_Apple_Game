import pygame
from pygame.locals import *
import time
import random

SIZE = 40

BACKGROUND_COLOR = (110,110,5)

class Apple:
    def __init__(self,parent_surface):
        self.parent_surface = parent_surface
        self.image = pygame.image.load("resources/transparent_apple.png").convert()
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_surface.blit(self.image,(self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,24)*SIZE
        self.y = random.randint(1,19)*SIZE

class Snake:
    def __init__(self,parent_surface, length):
        self.parent_surface = parent_surface
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.direction = "down"

        self.length = length
        self.x = [SIZE]*length
        self.y = [SIZE]*length

    

    def move_left(self):
        self.direction="left"

    def move_right(self):
        self.direction='right'

    def move_up(self):
        self.direction="up"

    def move_down(self):
        self.direction="down"

    
    
    def walk(self):

        for i in range(self.length - 1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        if self.direction == "right":
            self.x[0] +=SIZE
        if self.direction == "left":
            self.x[0]-=SIZE
        if self.direction == "up":
            self.y[0] -=SIZE
        if self.direction == "down":
            self.y[0] +=SIZE

        self.draw()

    def draw(self):
        
        # self.parent_surface.fill((BACKGROUND_COLOR))
        pygame.draw.rect(self.parent_surface, (207, 185, 23), (self.x[0], self.y[0], SIZE, SIZE))
        # Eyes
        pygame.draw.circle(self.parent_surface, (255, 255, 255), (self.x[0] + 10, self.y[0] + 10), 4)
        pygame.draw.circle(self.parent_surface, (255, 255, 255), (self.x[0] + 30, self.y[0] + 10), 4)

        # for i in range(1, self.length):
        #     pygame.draw.rect(self.parent_surface, (207, 185, 23), (self.x[i], self.y[i], SIZE, SIZE))

        # pygame.display.flip()

        # pygame.draw.rect(self.parent_surface, (255, 0, 0), (self.x[0], self.y[0], SIZE, SIZE))
        for i in range(1,self.length):
            self.parent_surface.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length +=1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake And Apple Game")

        pygame.mixer.init()
        self.backgound_music()
        self.surface = pygame.display.set_mode((1000,800))
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)

    def backgound_music(self):
        pygame.mixer.music.load("resources/bg_music.mp3")
        pygame.mixer.music.play()

    def render_background(self):
        for x in range(0, 1000, SIZE):
            for y in range(0, 800, SIZE):
                pygame.draw.rect(self.surface, (57, 94, 5), (x, y, SIZE, SIZE))
        # for x in range(0, 1000, SIZE):
        #     for y in range(0, 800, SIZE):
        #         color = (random.randint(30, 60), random.randint(100, 180), random.randint(30, 60))
        #         pygame.draw.rect(self.surface, color, (x, y, SIZE, SIZE))
        # bg = pygame.image.load("resources/og.png")
        # self.surface.blit(bg,(0,0))
        

    def is_collision(self,x1,y1,x2,y2):
        if x1>=x2 and x1<x2+SIZE:
            if y1>=y2 and y1<y2+SIZE:
                return True
        return False
    
    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        
        #snake collide with apple
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        #snake collide with snake
        for i in range(2,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.play_sound("crash")
                raise "Collision Occured"
                


    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: { self.snake.length-1}",True,(200,200,200))
        self.surface.blit(score,(850,50))

    def show_game_over(self):
        self.render_background()
        # self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length-1}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))

        pygame.display.flip()

        pygame.mixer.music.pause()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                    elif event.type == QUIT:
                        running = False

            try:

                if not pause:        
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause=True
                self.reset()

            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()


    
    
    
    