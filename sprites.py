import pygame
import config
import math
import random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y):
        self.width, self.height = config.TILESIZE, config.TILESIZE
        sprite = pygame.Surface([self.width, self.height])
        sprite.blit(self.sheet, (0,0), (x, y, self.width, self.height))
        sprite.set_colorkey(config.black)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = config.PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)


        #DEFINES THE ATTRIBUTES X,Y,WIDTH,HEIGHT
        self.x, self.y = x * config.TILESIZE, y * config.TILESIZE
        self.x_change, self.y_change = 0, 0

        self.facing = "down"
        self.animation_loop = 1
        self.image = self.game.character_spritesheet.get_sprite(3, 2)


        
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.down_animations = [self.game.character_spritesheet.get_sprite(3, 2),
                           self.game.character_spritesheet.get_sprite(35, 2),
                           self.game.character_spritesheet.get_sprite(68, 2)]

        self.up_animations = [self.game.character_spritesheet.get_sprite(3, 34),
                         self.game.character_spritesheet.get_sprite(35, 34),
                         self.game.character_spritesheet.get_sprite(68, 34)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(3, 98),
                           self.game.character_spritesheet.get_sprite(35, 98),
                           self.game.character_spritesheet.get_sprite(68, 98)]

        self.right_animations = [self.game.character_spritesheet.get_sprite(3, 66),
                            self.game.character_spritesheet.get_sprite(35, 66),
                            self.game.character_spritesheet.get_sprite(68, 66)]


    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")
        self.x_change, self.y_change = 0, 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:

            #CAMERA
            
            for sprite in self.game.all_sprites:
                sprite.rect.x += config.PLAYER_SPEED
                
            self.x_change -= config.PLAYER_SPEED
            self.facing = "left"

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            #CAMERA
            for sprite in self.game.all_sprites:
                sprite.rect.x -= config.PLAYER_SPEED
            self.x_change += config.PLAYER_SPEED
            self.facing = "right"

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            #CAMERA
            #for sprite in self.game.all_sprites:
             #   sprite.rect.y += config.PLAYER_SPEED
            self.y_change -= config.PLAYER_SPEED
            self.facing = "up"

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:

            #CAMERA
            #for sprite in self.game.all_sprites:
             #   sprite.rect.y -= config.PLAYER_SPEED
            self.y_change += config.PLAYER_SPEED
            self.facing = "down"
        
        if keys[pygame.K_LSHIFT]:
            config.PLAYER_SPEED = 5
        else:
            config.PLAYER_SPEED = 3
    
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False
            
    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            progress = pygame.sprite.spritecollide(self, self.game.next, False)
            back = pygame.sprite.spritecollide(self, self.game.back, False)
            if back:
                self.game.new(config.tilemap12)
            if progress:
                self.game.new(config.tilemap2)

            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += config.PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= config.PLAYER_SPEED

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            progress = pygame.sprite.spritecollide(self, self.game.next, False)
            back = pygame.sprite.spritecollide(self, self.game.back, False)
            if back:
                self.game.new(config.tilemap12)
            if progress:
                self.game.new(config.tilemap2)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    #for sprite in self.game.all_sprites:
                     #   sprite.rect.y += config.PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    #for sprite in self.game.all_sprites:
                     #   sprite.rect.y -= config.PLAYER_SPEED

    def animate(self):        
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tilemap):

        self.game = game
        self._layer = config.ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.facing = random.choice(["left", "right"])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        config.tilemap = tilemap
        self.x, self.y = x * config.TILESIZE, y * config.TILESIZE
        self.x_change, self.y_change = 0, 0

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2)

        self.rect = self.image.get_rect()
        self.rect.y, self.rect.x = self.y, self.x
        self.left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98),
                           self.game.enemy_spritesheet.get_sprite(35, 98),
                           self.game.enemy_spritesheet.get_sprite(68, 98)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66),
                            self.game.enemy_spritesheet.get_sprite(35, 66),
                            self.game.enemy_spritesheet.get_sprite(68, 66)]

    
    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change, self.y_change = 0, 0

    def movement(self):
        if self.facing == "left":
            self.x_change -= config.ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "right"
        
        if self.facing == "right":
            self.x_change += config.ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "left"
    
    def animate(self):
        
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 66)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 98)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = config.BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.y, self.x = y * config.TILESIZE, x * config.TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960, 448)
        

        self.rect = self.image.get_rect()
        self.rect.y, self.rect.x = self.y, self.x

class Next(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tilemap):
        self.game = game
        self._layer = config.NEXT_LAYER
        self.groups = self.game.all_sprites, self.game.next
        pygame.sprite.Sprite.__init__(self, self.groups)
        config.tilemap = tilemap
        self.y, self.x = y * config.TILESIZE, x * config.TILESIZE

        self.image = self.game.rightarrow_spritesheet.get_sprite(0, 0)

        self.rect = self.image.get_rect()
        self.rect.y, self.rect.x = self.y, self.x

class Back(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tilemap):
        self.game = game
        self._layer = config.NEXT_LAYER
        self.groups = self.game.all_sprites, self.game.back
        pygame.sprite.Sprite.__init__(self, self.groups)

        config.tilemap = tilemap
        self.y, self.x = y * config.TILESIZE, x * config.TILESIZE

        self.image = self.game.leftarrow_spritesheet.get_sprite(0, 0)

        self.rect = self.image.get_rect()
        self.rect.y, self.rect.x = self.y, self.x

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = config.GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.y, self.x = y * config.TILESIZE, x * config.TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 352)

        self.rect = self.image.get_rect()
        self.rect.y, self.rect.x = self.y, self.x

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font("Berlin_sans.ttf", fontsize)
        self.content = content
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.fg, self.bg = fg, bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            else:
                return False
        return False

class Attack(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = config.PLAYER_LAYER
        self.x, self.y = x, y
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)


        self.animation_loop = 0
        self.image = self.game.attack_spritesheet.get_sprite(0,0)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.right_animations = [self.game.attack_spritesheet.get_sprite(0, 64),
                           self.game.attack_spritesheet.get_sprite(32, 64),
                           self.game.attack_spritesheet.get_sprite(64, 64),
                           self.game.attack_spritesheet.get_sprite(96, 64),
                           self.game.attack_spritesheet.get_sprite(128, 64)]

        self.down_animations = [self.game.attack_spritesheet.get_sprite(0, 32),
                           self.game.attack_spritesheet.get_sprite(32, 32),
                           self.game.attack_spritesheet.get_sprite(64, 32),
                           self.game.attack_spritesheet.get_sprite(96, 32),
                           self.game.attack_spritesheet.get_sprite(128, 32)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(0, 96),
                           self.game.attack_spritesheet.get_sprite(32, 96),
                           self.game.attack_spritesheet.get_sprite(64, 96),
                           self.game.attack_spritesheet.get_sprite(96, 96),
                           self.game.attack_spritesheet.get_sprite(128, 96)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite(0, 0),
                         self.game.attack_spritesheet.get_sprite(32, 0),
                         self.game.attack_spritesheet.get_sprite(64, 0),
                         self.game.attack_spritesheet.get_sprite(96, 0),
                         self.game.attack_spritesheet.get_sprite(128, 0)]

    def update(self):
        self.animate()
        self.collide()
    
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing
        
        if direction == "up":
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == "down":
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        
        if direction == "left":
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        
        if direction == "right":
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
            


