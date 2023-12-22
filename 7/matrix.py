import os
import pygame as pg
from random import choice, randrange
#------------------------------------------------------------
class Symbol:
    #------------------------------------------------------------
    def __init__(self, x, y, speed, chars, pygame):
        self.x ,self.y = y = x, y
        self.speed = speed
        self.value = choice( chars['green'] )
        self.interval = randrange(5, 30)
        self.pygame = pygame
        self.chars = chars
    #------------------------------------------------------------
    #------------------------------------------------------------
    def draw(self, color):
        frames = self.pygame.time.get_ticks()
        if not frames % self.interval:
            self.value = choice( self.chars['green'] if color == 'green' else self.chars['lightgreen'] ) #choice -> Return a random element from the non-empty sequence seq
        self.y = self.y + self.speed if self.y < HEIGHT else (-FONT_SIZE)
        surface.blit(self.value, (self.x, self.y)) #blit modifies the destination surface by drawing at the specified coordinates.
    #------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
class SymbolColumn:
    #------------------------------------------------------------
    def __init__(self, x, y):
        self.column_height = randrange(8,18)
        self.speed = randrange(2,6)
        self.symbols = [ Symbol(x, i, self.speed, chars=chars_dict , pygame=pg) for i in range(y, y - FONT_SIZE * self.column_height, - FONT_SIZE) ]
    #------------------------------------------------------------
    #------------------------------------------------------------
    def draw(self):
        # if i == 0 then draw light green
        [  symbol.draw('green') if i else symbol.draw('lightgreen')   for i, symbol in enumerate(self.symbols) ]
    #------------------------------------------------------------
#------------------------------------------------------------


#------------------------------------------------------------
def create_chars(font_name, font_size):
    #int('0x30a0', 16) - > convert the hexadecimal '0x30a0' (base 16) to int = 12448
    # the original reference to katakana chars is: u+30AX which means '0x30a0' in hex, but for simplicity we use the int value
    # katakana = [  chr( int('0x30a0', 16) + i )  for i in range(96) ]
    katakana = [  chr( 12448 + i )  for i in range(96) ]

    font = pg.font.Font(font_name, font_size) #"MS Mincho is a Japanese font that features serifs at the end of its strokes"
    font.bold = True


    #                                            ( R           G          B )  every char will have a different tint of green
    green_katakana = [  font.render(char, True,  ( 0, randrange(100,200), 0 )  )  for char in katakana ] # probably a C library, the first arg is text, the second is antialiasing, the third is color
    lightgreen_katakana = [  font.render(char, True, pg.Color('lightgreen'))  for char in katakana ]
    chars_dict = {'green' : green_katakana, 'lightgreen' : lightgreen_katakana, 'plain' : katakana , 'font_size' : font_size, 'font_name' : font_name}


    return chars_dict
#------------------------------------------------------------
#------------------------------------------------------------
def handle_events(pygame):
    for i in pygame.event.get():
        if i.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            exit()

    
#------------------------------------------------------------

#------------------------------------------------------------
# def matrix():
os.environ['SDL_VIDEO_CENTERED'] = '1'
RES = WIDTH, HEIGHT = 1600, 900 #tuple (1600,900)
FONT_SIZE = 40
alpha_value = 0

pg.init()
screen = pg.display.set_mode(RES)
surface = pg.Surface(RES)
surface.set_alpha(alpha_value) # set the alpha value for the whole surface

clock = pg.time.Clock()

#----------------
chars_dict = create_chars(font_name='MS Mincho.ttf', font_size=FONT_SIZE)
#----------------



# symbol = Symbol(WIDTH//2 - FONT_SIZE//2, HEIGHT//2 - FONT_SIZE//2, speed=5)
symbol_columns = [ SymbolColumn(x,randrange(-HEIGHT, 0)) for x in range(0, WIDTH , FONT_SIZE) ]
while True:
    screen.blit(surface, (0,0))
    surface.fill(pg.Color('black'))

    [ symbol_column.draw() for symbol_column in symbol_columns ]

    if not pg.time.get_ticks() % 20 and alpha_value < 170:
        alpha_value += 5
        surface.set_alpha(alpha_value)

    # [exit() for i in pg.event.get() if i.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]]
    handle_events(pygame=pg)
    pg.display.flip() # make all changes made to the screen Surface visible by flipping the offscreen buffer with the onscreen buffer

    clock.tick(60) # control the framerate to 60 FPS
#------------------------------------------------------------
# matrix()