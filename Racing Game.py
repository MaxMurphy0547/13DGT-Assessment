import pygame

pygame.init()


screen = pygame.display.set_mode((650, 800))
game_icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("2D Car Racing Game")

clock = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf", 40)

black = (0, 0, 0)

car_image = pygame.image.load('player_car.png')
map_image = pygame.image.load('map.png')
map_image = pygame.transform.scale(map_image, (650, 800))
traffic_1_image = pygame.image.load('car_1.png')
traffic_2_image = pygame.image.load('car_2.png')
traffic_3_image = pygame.image.load('car_3.png')
traffic_4_image = pygame.image.load('car_4.png')
traffic_5_image = pygame.image.load('car_5.png')


class traffic:
    def __init__(self, x, y, image, speed):
        self.image = image
        self.x = x
        self.y = y
        self.speed = speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += self.speed
        if self.y > 800:
            self.y = -100 


    
traffic_1 = traffic(100, -100, traffic_1_image, 5)
traffic_2 = traffic(220, -300, traffic_2_image, 5)
traffic_3 = traffic(340, -500, traffic_3_image, 5)
traffic_4 = traffic(100, -700, traffic_4_image, 5)
traffic_5 = traffic(220, -900, traffic_5_image, 5)

traffic_list = [traffic_1, traffic_2, traffic_3, traffic_4, traffic_5]

class MovingBackground:
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
    current_speed = 0
    initial_speed = 20  
    start = False

    background = MovingBackground(map_image, 0)
    
    while not quit_game:
        if not start:
            start_message("Press Space To Start", black)
        pygame.display.update()
        dt = clock.tick(40) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if car_y == 750:
                        start = True
                        car_y_change = -20
                elif start:
                    if car_y <= y_start_position:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            quit()
                        elif event.key == pygame.K_LEFT:
                            car_x_change = -15
                        elif event.key == pygame.K_RIGHT:
                            car_x_change = 15
            elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        car_x_change = 0
                    elif event.key == pygame.K_RIGHT:
                        car_x_change = 0

        
        if car_y > y_start_position:
            car_y += car_y_change
            if car_y <= y_start_position:
                car_y = y_start_position
                car_y_change = 0
                current_speed = initial_speed
                background.speed = current_speed
        else:
            background.update()

        if car_y == y_start_position:
            for traffic in traffic_list:
                traffic.move()

        if car_x + car_x_change < 80:
            car_x = 80
        elif car_x + car_x_change > 480:
            car_x = 480
        else:
            car_x += car_x_change

        for traffic in traffic_list:
            traffic.draw()
        
        background.draw()
        
        for traffic in traffic_list:
            traffic.draw()

        screen.blit(car_image, (car_x, car_y))
        pygame.display.update()
        clock.tick(40)

game_loop()
