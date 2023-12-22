import os
import pygame as pg
from random import choice, randrange
#------------------------------------------------------------
class SpecialChar: #Japanese Katakana
    #------------------------------------------------------------
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = None
        self.interval = randrange(5, 30)
    #------------------------------------------------------------
    #------------------------------------------------------------
    def draw(self, color, surface, speed, chars, pygame, screen_resolution):
        frames = pygame.time.get_ticks()
        font_size = chars['font_size']
        screen_width , screen_height = screen_resolution
        
        #-------
        if (frames % self.interval) == 0 or self.value == None: #this makes the chars flick given a certain interval
            #now considering we are flicking the chars, we need to identify if this is the first char of the column, the first char is always light green
            if color == 'green':
                self.value = choice( chars['green'] )
            else:
                self.value = choice( chars['lightgreen'] )
        #-------

        if self.y < screen_height:
            self.y = self.y + speed
        else:
            self.y = -font_size

        surface.blit(self.value, (self.x, self.y)) #blit modifies the destination surface by drawing at the specified coordinates.
    #------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
class CharColumn:
    #------------------------------------------------------------
    def __init__(self, x, y, chars, pygame, screen_resolution):
        self.column_height = randrange(8,18)
        self.speed = randrange(2,6)
        font_size = chars['font_size']
        self.chars = chars
        self.pygame = pygame
        self.screen_resolution = screen_resolution

        self.symbols = []
        for_to_limit = y - font_size * self.column_height
        for i in range(y, for_to_limit, -font_size ):
            temp = SpecialChar(x, i) 
            self.symbols.append(temp)

    #------------------------------------------------------------
    #------------------------------------------------------------
    def draw(self, surface):

        for i , i_char in enumerate(self.symbols):
            if i == 0 : #first char in the column
                i_char.draw('lightgreen',surface, self.speed, chars = self.chars, pygame = self.pygame, screen_resolution=self.screen_resolution)
            else:
                i_char.draw('green',surface, self.speed, chars = self.chars, pygame = self.pygame, screen_resolution=self.screen_resolution)
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


    #                                                 ( R           G          B )  every char will have a different tint of green
    green_katakana =      [  font.render(char, True,  ( 0, randrange(100,200), 0 )  )  for char in katakana ] # probably a C library, the first arg is text, the second is antialiasing, the third is color
    lightgreen_katakana = [  font.render(char, True, pg.Color('lightgreen')         )  for char in katakana ]
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
def intro_fade(pygame, p_surface, p_alpha_value):
    if not pygame.time.get_ticks() % 20 and p_alpha_value < 170:
        p_alpha_value += 5
        p_surface.set_alpha(p_alpha_value)
    
    return p_surface, p_alpha_value
#------------------------------------------------------------            
#------------------------------------------------------------            
def create_char_column(screen_resolution, chars_dict, pygame):
    screen_width , screen_height = screen_resolution
    font_size = chars_dict['font_size']

    #-----
    symbol_columns = []
    for x in range(0, screen_width , font_size):
        y = randrange(-screen_height, 0)
        temp = CharColumn(x,y, chars=chars_dict, pygame=pygame ,screen_resolution=screen_resolution) 
        symbol_columns.append(temp)
    #-----

    return symbol_columns
#------------------------------------------------------------            

#------------------------------------------------------------
def matrix():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    SCREEN_RESOLUTION = SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900 #tuple (1600,900)
    FONT_SIZE = 40
    alpha_value = 0

    pg.init()
    #----------------
    pg.display.set_caption('Matrix')
    screen = pg.display.set_mode(SCREEN_RESOLUTION)
    surface = pg.Surface(SCREEN_RESOLUTION)
    surface.set_alpha(alpha_value) # set the alpha value for the whole surface
    #----------------
    clock = pg.time.Clock()
    #----------------
    chars_dict = create_chars(font_name='MS Mincho.ttf', font_size=FONT_SIZE)
    #----------------

    symbol_columns = create_char_column(screen_resolution=SCREEN_RESOLUTION, chars_dict = chars_dict, pygame = pg)
    while True:
        screen.blit(surface, (0,0))
        surface.fill(pg.Color('black'))

        [ symbol_column.draw(surface=surface) for symbol_column in symbol_columns ]

        surface, alpha_value = intro_fade(pygame=pg, p_surface=surface, p_alpha_value=alpha_value)

        handle_events(pygame=pg) #keyboard keys, mouse, etc

        pg.display.flip() # make all changes made to the screen Surface visible by flipping the offscreen buffer with the onscreen buffer

        clock.tick(60) # control the framerate to 60 FPS
#------------------------------------------------------------
matrix()