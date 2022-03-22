import pygame
import sys
import sprites, config

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIN_width, config.WIN_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('Berlin_sans.ttf', 32)

        self.character_spritesheet = sprites.Spritesheet("img/character.png")
        self.terrain_spritesheet = sprites.Spritesheet("img/terrain.png")
        self.rightarrow_spritesheet = sprites.Spritesheet("img/rightarrow.png")
        self.leftarrow_spritesheet = sprites.Spritesheet("img/leftarrow.png")
        self.enemy_spritesheet = sprites.Spritesheet("img/enemy.png")
        self.attack_spritesheet = sprites.Spritesheet("img/attack.png")
        self.intro_background = pygame.image.load("./img/introbackground.png")
        self.go_background = pygame.image.load("./img/gameover.png")

    def createTilemap(self, tilemap):
        for tile_y,row in enumerate(tilemap):
            for tile_x, column in enumerate(row):
                args1 = (self, tile_x, tile_y)
                sprites.Ground(*args1)
                if column == "B":
                    sprites.Block(*args1)
                if column == "P":
                    self.player = sprites.Player(*args1)
                if column == "N":
                    sprites.Next(*args1, tilemap)
                if column == "R": 
                    sprites.Back(*args1, tilemap)
                if column == "E": 
                    sprites.Enemy(*args1, tilemap)

    def new(self, tilemap = config.tilemap1):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.next = pygame.sprite.LayeredUpdates()
        self.back = pygame.sprite.LayeredUpdates()
        self.createTilemap(tilemap)

        if tilemap == config.tilemap12:
            for sprite in self.all_sprites:
                sprite.rect.x -= 800
        else:
            for sprite in self.all_sprites:
                sprite.rect.x -= config.WIN_height /2   

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == "up":
                        sprites.Attack(self, self.player.rect.x, self.player.rect.y - config.TILESIZE)
                    if self.player.facing == "down":
                        sprites.Attack(self, self.player.rect.x, self.player.rect.y + config.TILESIZE)
                    if self.player.facing == "left":
                        sprites.Attack(self, self.player.rect.x - config.TILESIZE, self.player.rect.y)
                    if self.player.facing == "right":
                        sprites.Attack(self, self.player.rect.x + config.TILESIZE, self.player.rect.y)


    def update(self):
        # game loop updates
        self.all_sprites.update()

    def draw(self):

        # game loop draw
        self.screen.fill(config.black)
        self.all_sprites.draw(self.screen)
        self.clock.tick(config.FPS)
        pygame.display.update()
    
    def main(self):
        #game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text = self.font.render("Game Over", True, config.white)
        text_rect= text.get_rect(center=(config.WIN_width/2, config.WIN_height/2))
        restart_button = sprites.Button(10, config.WIN_height -60, 120, 50, config.white, config.black, "Restart", 32)
        exit_button = sprites.Button(config.WIN_width - 130, config.WIN_height -60, 120, 50, config.white, config.black, "Exit", 32)
        
        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()
            
            if exit_button.is_pressed(mouse_pos,mouse_pressed):
                self.running = False
            
            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            self.clock.tick(config.FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True
        title = self.font.render("Amazing Game", True, config.black)
        title_rect = title.get_rect(center=(config.WIN_width/2, 50))

        play_button = sprites.Button(260, config.WIN_height - 200, 100, 50, config.white, config.black, "Play", 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(config.FPS)
            pygame.display.update()


g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
pygame.quit()
sys.exit()