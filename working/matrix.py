import os
import pygame as pg
from random import choice, randrange

class Symbol:
    def __init__(self, x, y):
        self.x ,self.y = y = x, y
        self.value = choice(green_katakana)
        # self.interval = randrange(5, 30)

    def draw(self):
        frames = pg.time.get_ticks()
        # if not frames % self.interval:
        #     self.value = choice(green_katakana) #choice -> Return a random element from the non-empty sequence seq
        surface.blit(self.value, (self.x, self.y)) #blit modifies the destination surface by drawing at the specified coordinates.

os.environ['SDL_VIDEO_CENTERED'] = '1'
RES = WIDTH, HEIGHT = 1600, 900 #tuple (1600,900)
FONT_SIZE = 40
pg.init()
surface = pg.display.set_mode(size= RES)
clock = pg.time.Clock()

#int('0x30a0', 16) - > convert the hexadecimal '0x30a0' (base 16) to int = 12448
# the original reference to katakana chars is: u+30AX which means '0x30a0' in hex, but for simplicity we use the int value
# katakana = [  chr( int('0x30a0', 16) + i )  for i in range(96) ]
katakana = [  chr( 12448 + i )  for i in range(96) ]

font = pg.font.Font('MS Mincho.ttf', FONT_SIZE) #"MS Mincho is a Japanese font that features serifs at the end of its strokes"
font.bold = True
green_katakana = [  font.render(char, True, pg.Color('green'))  for char in katakana ] # probably a C library, the first arg is text, the second is antialiasing, the third is color

symbol = Symbol(0,0)
while True:
    surface.fill(pg.Color('black'))

    symbol.draw()

    [exit() for i in pg.event.get() if i.type == pg.QUIT]
    pg.display.flip() # make all changes made to the screen Surface visible by flipping the offscreen buffer with the onscreen buffer

    clock.tick(60) # control the framerate to 60 FPS
