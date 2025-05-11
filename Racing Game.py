import pygame
pygame.init()

screen = pygame.display.set_mode((650, 800))
game_icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("2D Car Racing Game")

clock = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf", 40)

green = (188, 227, 199)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

car_image = pygame.image.load('player_car.png')
car_rect = car_image.get_rect()

map_image = pygame.image.load('map.png')
map_rect = map_image.get_rect()
map_image = pygame.transform.scale(map_image, (650, 800))


def game_loop():
    quit_game = False
    car_x = 280
    car_y = 750
    

    while not quit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = true
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        screen.fill(white)
        screen.blit(map_image, (0, 0))
        screen.blit(car_image, (car_x, car_y))
        
        pygame.display.update()
        clock.tick(60)



game_loop()

