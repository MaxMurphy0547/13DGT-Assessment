import pygame
import time
pygame.init()

screen = pygame.display.set_mode((650, 800))
pygame.display.set_caption("2D Car Racing Game")
clock = pygame.time.Clock()

car_image = pygame.image.load('player_car.png')
map_image = pygame.image.load('map.png')
game_icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(game_icon)


class car:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self):
        screen.blit(self.image, self.rect)


class movingbackground:
    def __init__(self, image, speed):
        self.image = image
        self.speed = speed
        self.map1 = 0
        self.map2 = -screen.get_height()

    def update(self):
        self.map1 += self.speed
        self.map2 += self.speed
        if self.map1 >= screen.get_height():
            self.map1 = -screen.get_height()
        if self.map2 >= screen.get_height():
            self.map2 = -screen.get_height()

    def draw(self):
        screen.blit(self.image, (0, self.map1))
        screen.blit(self.image, (0, self.map2))


def game_loop():
    quit_game = False
    car_x = 280
    car_y = 750
    y_start_position = 590
    car_speed = 5
    car_x_change = 0
    car_y_change = 0
    start = False
    
    player_car = car(car_image, car_x, car_y)
    background = movingbackground(map_image, 5)
    
    
    while not quit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_SPACE:
                    start = True
                    car_y_change = -20
                elif start and car_y <= y_start_position:
                    if event.key == pygame.K_LEFT and player_car.rect.left > 80:
                        player_car.rect.x -= 20
                    elif event.key == pygame.K_RIGHT and player_car.rect.right < 570:
                        player_car.rect.x += 20
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    car_x_change = 0
                elif event.key == pygame.K_RIGHT:
                    car_x_change = 0
                    
        print (car_y)
        print (car_x)
                    
        if car_y <= y_start_position:
            background.update()

        
        car_x += car_x_change
        car_y += car_y_change
        
        if car_y < 600:
            car_y_change = 0
        if car_x == 80 or car_x == 480:
            car_x_change = 0

        background.draw()
        player_car.draw()
        
        pygame.display.update()
        clock.tick(40)



game_loop()
