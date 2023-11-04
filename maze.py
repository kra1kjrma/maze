import pygame
import time

WIDTH = 700
HEIGHT = 500
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабіринт")
background = pygame.transform.scale(
    pygame.image.load("background.jpg"),
    (WIDTH, HEIGHT)
)

clock = pygame.time.Clock()

pygame.font.init()

pygame.mixer.init()
pygame.mixer.music.load("jungles.ogg")
pygame.mixer.music.play()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename, x,y, speed):
        super().__init__()
        self.image  = pygame.transform.scale(
            pygame.image.load(filename), (65,65)
        )

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = x
        
        self.speed = speed
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed

        if keys_pressed[pygame.K_DOWN] and self.rect.y < HEIGHT-70:
            self.rect.y += self.speed

        if keys_pressed[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

        if keys_pressed[pygame.K_RIGHT] and self.rect.x < WIDTH-70:
            self.rect.x += self.speed

class Enemy(GameSprite):
    direction = "left"
    def update(self):
        if self.rect.x < WIDTH/2:    self.direction = "right"
        elif self.rect.x > WIDTH - 65:
            self.direction = "left"
        
        if self.direction == "right":
            self.rect.x += self.speed

        if self.direction == "left":
            self.rect.x -= self.speed
        
class Wall(pygame.sprite.Sprite):
    def __init__(self, coords, size, color):
        self.rect = pygame.Rect(coords, size)
        self.color = color
    def draw_wall(self):
        pygame.draw.rect(window, self.color, self.rect)

player = Player("hero.png", 50, HEIGHT-50, 5)

gold = GameSprite("treasure.png", WIDTH-250, HEIGHT-450, 0)

enemy = Enemy("cyborg.png", WIDTH/2-100, HEIGHT/3, 3)

walls = [
    Wall((10,10), (WIDTH-20, 10), (255,0,0)),
    Wall((WIDTH-10,10), (200, HEIGHT), (255,0,0)),
    Wall((10,10), (10, HEIGHT-20), (0,0,255)),
    Wall((10,HEIGHT-10), (WIDTH-20, 10), (255,0,0)),
    Wall((WIDTH/4, HEIGHT-10), (WIDTH/2, 10), (0,255,0)),
    Wall((WIDTH/2-100, HEIGHT/2), (10, HEIGHT/2), (0,255,0)),
    Wall((WIDTH/4, 10), (WIDTH/2, 10), (0,255,0)),
    Wall((WIDTH/2+100, 10), (10, HEIGHT/2), (0,255,0)),
]

game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    window.blit(background, (0,0))
    gold.reset()
    gold.update()
    enemy.reset()
    enemy.update()
    player.reset()
    player.update()
    for w in walls:
        w.draw_wall()
    
    wall_collision =  any([pygame.sprite.collide_rect(player, w) for w in walls])

    if pygame.sprite.collide_rect(player, enemy) or wall_collision:
        sfx = pygame.mixer.Sound("kick.ogg")
        sfx.play()
        font = pygame.font.Font(None, 40)
        text = font.render("YOU LOSE", True, (255,0,0))
        window.blit(text, (WIDTH/2, HEIGHT/2))
        time.sleep(1)
        game_over = True

    if pygame.sprite.collide_rect(player, gold):
        sfx = pygame.mixer.Sound("money.ogg")
        sfx.play()
        font = pygame.font.Font(None, 40)
        text = font.render("YOU WIN", True, (0,255,0))
        window.blit(text, (WIDTH/2, HEIGHT/2))
        time.sleep(3)
        game_over = True
        

    pygame.display.update()
    clock.tick(60)