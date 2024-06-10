import pygame
from pygame.locals import *
import random
# from pygame.sprite import _Group

class Bird(pygame.sprite.Sprite):
  def __init__(self, x, y) -> None:
    #super().__init__(self)
    pygame.sprite.Sprite.__init__(self)

    self.index = 0
    self.counter = 0
    self.images = []

    for num in range(1, 4):
      img = pygame.image.load(f'img/bird{num}.png')
      self.images.append(img)

    self.image = self.images[self.index]
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]

    self.velocity = 0

    self.clicked = False

  def update(self):

    if flying == True:

      self.velocity += 0.5

      if self.velocity > 8:
        self.velocity = 8

      if self.rect.bottom < 768:
        self.rect.y += int(self.velocity)

    if game_over == False:        

      if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
        self.clicked = True
        self.velocity = -10

      if pygame.mouse.get_pressed()[0] == 0:
        self.clicked = False
      
      # handle the animation
      self.counter += 1
      flap_cooldown = 5

      if self.counter > flap_cooldown:
        self.counter = 0
        self.index += 1

        if self.index >= len(self.images):
          self.index = 0

      self.image = self.images[self.index]

      # rotate the bird
      self.image = pygame.transform.rotate(self.images[self.index], self.velocity)
    else:
      self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
  def __init__(self, x, y, pos, pipe_gap = 200, scroll_speed = 4) -> None:
    pygame.sprite.Sprite.__init__(self)
    
    self.image = pygame.image.load('img/pipe.png')
    self.rect = self.image.get_rect()

    self.pipe_gap = pipe_gap
    self.scroll_speed = scroll_speed

    if pos == 1:
      self.image = pygame.transform.flip(self.image, False, True)
      self.rect.bottomleft = [x, y - int(self.pipe_gap / 2)]
    else:
      self.rect.topleft = [x, y + int(self.pipe_gap / 2)]

  def update(self):
    self.rect.x -= self.scroll_speed
    
    if self.rect.right < 0:
      self.kill()

class Button():
  def __init__(self, x, y, image) -> None:
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)

  def draw(self):

    action = False

    pos = pygame.mouse.get_pos()

    if self.rect.collidepoint(pos):
      if pygame.mouse.get_pressed()[0] == 1:
        action = True

    screen.blit(self.image, (self.rect.x, self.rect.y))

    return action

def draw_text(text, font, text_color, x, y):
  img = font.render(text, True, text_color)
  screen.blit(img, (x, y))

def reset_game():
  pipe_group.empty()

  flappy.rect.x, flappy.rect.y = 100, int(screen_height / 2)

  score = 0

  return score

if __name__ == '__main__':
  pygame.init()

  screen_width = 864
  screen_height = 936

  screen = pygame.display.set_mode((screen_width, screen_height))

  pygame.display.set_caption('Flappy Bird')

  bg = pygame.image.load('img/bg.png')

  ground = pygame.image.load('img/ground.png')

  reset_button_img = pygame.image.load('img/restart.png')

  font = pygame.font.SysFont('Bauhaus 93', 60)

  white = (255, 255, 255)

  run = True

  flying = False

  game_over = False

  pipe_frequency = 2500 #milliseconds

  last_pipe = pygame.time.get_ticks() - pipe_frequency

  ground_scroll = 0

  scroll_speed = 4

  fps = 30

  clock = pygame.time.Clock()

  bird_group = pygame.sprite.Group()
  pipe_group = pygame.sprite.Group()

  flappy = Bird(100, int(screen_height / 2))

  # pipe_hegiht = 100
  # bottom_pipe = Pipe(300, int(screen_height / 2) + pipe_hegiht, -1)
  # top_pipe = Pipe(300, int(screen_height / 2) - pipe_hegiht, 1)

  bird_group.add(flappy)

  button = Button(screen_width//2 - 50, screen_height//2 - 100, reset_button_img)

  # pipe_group.add(bottom_pipe)
  # pipe_group.add(top_pipe)

  score = 0
  pass_pipe = False

  while run:

    clock.tick(fps)

    # Note: Rendering level

    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    #pipe_group.update()

    screen.blit(ground, (ground_scroll, 768))

    # check score
    if len(pipe_group) > 0:
      if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
        and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
        and pass_pipe == False:
          pass_pipe = True
      if pass_pipe == True:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
          score += 1
          pass_pipe = False
      #print(score)

    draw_text(str(score), font, white, int(screen_height/2), 20)

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
      game_over = True

    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    # stop update ground_scroll
    if game_over == False and flying == True:
      #generate new pipes
      time_now = pygame.time.get_ticks()
      if time_now - last_pipe > pipe_frequency:
        pipe_height = random.randint(-100, 100)
        bottom_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
        top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)

        pipe_group.add(bottom_pipe)
        pipe_group.add(top_pipe)

        last_pipe = time_now

      ground_scroll -= scroll_speed

      if abs(ground_scroll) > 35:
        ground_scroll = 0


      pipe_group.update()
      
    # reset
    if game_over == True:
      if button.draw() == True:
        game_over = False
        score = reset_game()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      
      if event.type == pygame.MOUSEBUTTONDOWN and flying == False:
        flying = True

    pygame.display.update()

  pygame.quit()