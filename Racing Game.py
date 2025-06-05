import pygame
import time
pygame.init()


screen = pygame.display.set_mode((650, 800))
game_icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("2D Car Racing Game")

clock = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf", 40)

black = (0, 0, 0)


car_image = pygame.image.load('player_car.png')
car_rect = car_image.get_rect()
map_image = pygame.image.load('map.png')
map_rect = map_image.get_rect()
map_image = pygame.transform.scale(map_image, (650, 800))




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

def start_message(msg, text_colour):
    txt = font.render(msg, True, text_colour)
    text_box = txt.get_rect(center=(325, 100))
    screen.blit(txt, text_box)



        
def game_loop():
    quit_game = False
    car_x = 280
    car_y = 750
    y_start_position = 590
    car_x_change = 0
    car_y_change = 0
    accelerating = 50
    braking = 50
    current_speed = 0
    target_speed = 0
    max_speed = 200
    min_speed = 10
    
    start = False
    car_accelerating = False
    car_braking = False
    initial_speed = 0
    
    player_car = (car_image, car_x, car_y)
    background = movingbackground(map_image, 10)
    
    while not quit_game:
        print(current_speed)
        if start == False:
            start_message("Press Space To Start", black)
        pygame.display.update()
        dt = clock.tick(40) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_SPACE:
                    if car_y == 750:
                        start = True
                        car_y_change = -20
                        initial_speed = abs(car_y_change)
                        start_message("", black)
                elif start:
                    if car_y <= y_start_position:
                        if event.key == pygame.K_LEFT:
                            car_x_change = -10
                        elif event.key == pygame.K_RIGHT:
                            car_x_change = 10
                        elif event.key == pygame.K_UP:
                            car_accelerating = True
                        elif event.key == pygame.K_DOWN:
                            car_braking = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    car_x_change = 0
                elif event.key == pygame.K_RIGHT:
                    car_x_change = 0
                elif event.key == pygame.K_UP:
                    car_accelerating = False
                elif event.key == pygame.K_DOWN:
                    car_braking = False

        if car_accelerating:
            target_speed = max_speed
        elif car_braking:
            target_speed = min_speed
        else:
            target_speed = current_speed

        if current_speed < target_speed:
            current_speed += accelerating * dt
            if current_speed > target_speed:
                current_speed = target_speed
        elif current_speed > target_speed:
            current_speed -= braking * dt
            if current_speed < target_speed:
                current_speed = target_speed
        
        
        if car_y > y_start_position:
            car_y += car_y_change
            if car_y <= y_start_position:
                car_y = y_start_position
                car_y_change = 0
                current_speed = initial_speed 
        else:
            background.speed = current_speed
            background.update()


        if car_x + car_x_change < 80:
            car_x = 80
            car_x_change = 0
        elif car_x + car_x_change > 480:
            car_x = 480
            car_x_change = 0
        else:
            car_x += car_x_change

            
        car_x += car_x_change
        
        background.draw()
        screen.blit(car_image, (car_x, car_y))
        pygame.display.update()
        clock.tick(40)



game_loop()
