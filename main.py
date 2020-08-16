'''
PONG! 🏓
Zul Hilmi, 16 / 8 / 2020
'''

import pygame, random, math
from pygame import gfxdraw

# SETUP
pygame.init()
size    = width, height = 900, 600
display = pygame.display.set_mode((size))
pygame.display.set_caption("PONG! 🏓")

# WARNA
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GREY   = (100, 100, 100)
YELLOW = (200, 220, 50)
BLUE   = (100, 100, 200)
GREEN  = (100, 200, 100)
RED    = (200, 100, 100)

# INFOBAR
font           = pygame.font.SysFont("Prototype", 20, bold=False)
infobar_width  = width
infobar_height = 50

def framerate(frate):
  # SET UNTUK FRAMERATE
  clock = pygame.time.Clock()
  clock.tick(frate)

def info_bar(SKOR_PLAYER_1, SKOR_PLAYER_2):
  pygame.draw.rect(display, GREY, (0, 0, infobar_width, infobar_height))
  text_skor_player_1       = font.render("SKOR: "+str(SKOR_PLAYER_1), True, WHITE)
  text_skor_player_2       = font.render("SKOR: "+str(SKOR_PLAYER_2), True, WHITE)
  text_instruksi           = font.render("Tekan SPASI to MAIN", True, WHITE)
  textRect_player_1        = text_skor_player_1.get_rect()
  textRect_player_2        = text_skor_player_2.get_rect()
  textRect_instruksi       = text_instruksi.get_rect()
  textRect_player_1.center = (width - 100, infobar_height // 2)
  textRect_player_2.center = (100, infobar_height // 2)
  textRect_instruksi.center = (width / 2, infobar_height // 2)
  display.blit(text_skor_player_1, textRect_player_1)
  display.blit(text_skor_player_2, textRect_player_2)
  if not bola.ready:
    display.blit(text_instruksi, textRect_instruksi)


# MEJA
meja_line_width_h = 1
meja_line_width_v = 7
def garis_meja():
  pygame.draw.line(display, WHITE, (width/2, 0+infobar_height), (width/2, height), width=meja_line_width_v)
  pygame.draw.line(display, WHITE, (0, height / 2), (width, height / 2), width=meja_line_width_h)
  pygame.draw.rect(display, WHITE, (0, 0+infobar_height, width, height-infobar_height), width=meja_line_width_v)


# PLAYER
class Player:
  def __init__(self, x, y, player):
    self.w      = 20
    self.h      = 100
    self.space  = 20
    self.x      = x
    self.y      = y
    self.color  = GREEN
    self.player = player # posisi player: 'left' dan 'righ'
    self.up     = False
    self.down   = False
    self.step   = 10

  def tampilkan(self):
    if self.player == 'right':
      pygame.draw.rect(display, self.color, (self.x - self.space - self.w, self.y - self.h / 2, self.w, self.h), border_radius=7)
    else:
      pygame.draw.rect(display, self.color, (self.x + self.space, self.y - self.h / 2, self.w, self.h), border_radius=7)

  def update(self):
    if self.up:
      self.y = self.y - self.step
    if self.down:
      self.y = self.y + self.step

  def cekTepi(self):
    if self.y > height - self.h / 2:
      self.y = height - self.h / 2
      self.color = RED
    elif self.y < infobar_height * 2:
      self.y = infobar_height * 2
      self.color = RED
    else:
      self.color = GREEN


# BOLA
class Bola():
  def __init__(self):
    self.r     = 15
    self.x     = width / 2
    self.y     = height / 2
    self.color = YELLOW
    self.stepX = 10
    self.stepY = 1.5
    self.ready = False
    self.win   = ''
    # if random.randint(1, 2) < 2:
    #   self.stepX *= -1
    if random.randint(1, 2) < 2:
      self.stepY *= -1

  def tampilkan(self):
    pygame.gfxdraw.aacircle(display, int(self.x), int(self.y), self.r, self.color)
    pygame.gfxdraw.filled_circle(display, int(self.x), int(self.y), self.r, self.color)

  def update(self):
    if self.ready:
      # jika player 1 (kanan) menang, maka bola akan dilempar ke kiri
      if self.win == 'right':
        self.stepX *= -1
      # jika player 2 (kiri) menang, maka bola akan dilempar ke ke kanan
      elif self.win == 'left':
        self.stepX *= 1
      self.x = self.x + self.stepX
      self.y = self.y - self.stepY
      self.win = '' # reset pemenang

  def cekTepi(self):
    if self.y < infobar_height + self.r or self.y > height - self.r - meja_line_width_v / 2:
      self.stepY *= -1

  def golRight(self, player_right):
    if self.x < 0:
      # reset all object and attr
      self.__init__()
      player_right.y = height / 2
      player_left.y = height / 2
      self.win = 'right'
      self.x = player_right.x - player_right.space - player_right.w - self.r
      return True

  def golLeft(self, player_left):
    if self.x > width:
      # reset all object and attr
      self.__init__()
      player_right.y = height / 2
      player_left.y = height / 2
      self.win = 'left'
      self.x = player_left.x + player_left.space + player_left.w + self.r
      return True

  def collisionRight(self):
    if self.y < player_right.y + player_right.h/2 and self.y > player_right.y - player_right.h/2 and self.x + self.r > player_right.x - player_right.w - player_right.space:
      self.stepX *= -1
  
  def collisionLeft(self):
    if self.y < player_left.y + player_left.h/2 and self.y > player_left.y - player_left.h/2 and self.x - self.r < player_left.x + player_left.w + player_left.space:
      self.stepX *= -1
    


# FUNGSI UTAMA
def main():
  SKOR_PLAYER_1  = 0
  SKOR_PLAYER_2  = 0
  run = True
  while run:
    # BACKGROUND
    display.fill(BLUE)

    # GARIS MEJA
    garis_meja()

    # PLAYER
    # right
    player_right.tampilkan()
    player_right.update()
    player_right.cekTepi()
    # left
    player_left.tampilkan()
    player_left.update()
    player_left.cekTepi()

    # BOLA
    bola.tampilkan()
    bola.update()
    bola.cekTepi()
    bola.collisionRight()
    bola.collisionLeft()
    if bola.golRight(player_right):
      SKOR_PLAYER_1 += 1
    if bola.golLeft(player_left):
      SKOR_PLAYER_2 += 1

    # INFOBAR / SKOR
    info_bar(SKOR_PLAYER_1, SKOR_PLAYER_2)

    # UPDATE TAMPILAN GAME
    framerate(90)
    pygame.display.update()

    # EVENTS
    for e in pygame.event.get():
      if e.type == pygame.KEYDOWN and e.key == pygame.K_i:
        player_right.up = True
      elif e.type == pygame.KEYDOWN and e.key == pygame.K_k:
        player_right.down = True
      elif e.type == pygame.KEYDOWN and e.key == pygame.K_w:
        player_left.up = True
      elif e.type == pygame.KEYDOWN and e.key == pygame.K_s:
        player_left.down = True
      elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
        bola.ready = True
      elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
        run = False
      if e.type == pygame.KEYUP:
        player_right.up = False
        player_right.down = False
        player_left.up = False
        player_left.down = False
      if e.type == pygame.QUIT:
        run = False



if __name__ == '__main__':
  player_right = Player(width, height / 2, 'right')
  player_left  = Player(0, height / 2, 'left')
  
  bola         = Bola()

  main()