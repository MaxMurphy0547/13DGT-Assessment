import pygame
import time
import random
pygame.init()

screen = pygame.display.set_mode((650, 800))
game_icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("2D Car Racing Game")

clock = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf", 40)
death_font = pygame.font.Font("freesansbold.ttf", 30)


white = (255, 255, 255)
black = (0, 0, 0)

car_image = pygame.image.load('player_car.png')
map_image = pygame.image.load('map.png')
map_image = pygame.transform.scale(map_image, (650, 800))
traffic_1_image = pygame.image.load('car_1.png')
traffic_2_image = pygame.image.load('car_2.png')
traffic_3_image = pygame.image.load('car_3.png')
traffic_4_image = pygame.image.load('car_4.png')
traffic_5_image = pygame.image.load('car_5.png')

lanes = [115, 280, 430]


class Traffic:
    def __init__(self, lane, image, speed):
        self.image = image
        self.x = lane
        self.y = random.randint(-1500, -100)
        self.speed = speed
        self.passed = False

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self, all_traffic):
        self.y += self.speed
        if self.y > 800:
            while True:
                new_y = random.randint(-1500, -100)
                new_x = random.choice(lanes)

                is_overlapping = False
                for car in all_traffic:
                    if car is not self and car.x == new_x and abs(car.y - new_y) < 150:
                        is_overlapping = True
                        break

                if not is_overlapping:
                    self.x = new_x
                    self.y = new_y
                    self.passed = False
                    break

def generate_traffic():
    traffic_list = []
    traffic_images = [traffic_1_image, traffic_2_image, traffic_3_image, traffic_4_image, traffic_5_image]
    speed = 4

    for _ in range(5):
        while True:
            lane = random.choice(lanes)
            y = random.randint(-1500, -100)
            image = random.choice(traffic_images)

            is_overlapping = False
            for car in traffic_list:
                if car.x == lane and abs(car.y - y) < 150:
                    is_overlapping = True
                    break

            if not is_overlapping:
                new_car = Traffic(lane, image, speed)
                new_car.y = y
                traffic_list.append(new_car)
                break

    return traffic_list



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

def load_high_score():
    try:
        with open("HI_score_Racing.txt", 'r') as hi_score_file:
            return int(hi_score_file.read())
    except:
        return 0 

def save_high_score(high_score):
    with open("HI_score_Racing.txt", 'w') as hi_score_file:
        hi_score_file.write(str(high_score))


def score_message(msg, text_colour):
    txt = font.render(msg, True, text_colour)
    text_box = txt.get_rect(center=(150, 50))
    screen.blit(txt, text_box)

def high_score_message(msg, text_colour):
    txt = font.render(msg, True, text_colour)
    text_box = txt.get_rect(center=(500, 50))
    screen.blit(txt, text_box)

def death_message(msg, text_colour):
    txt = death_font.render(msg, True, text_colour)
    text_box = txt.get_rect(center=(325, 400))
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
    score = 0
    high_score = load_high_score()

    background = MovingBackground(map_image, 0)
    traffic_list = generate_traffic()

    while not quit_game:
        if not start:
            start_message("Press Space To Start", black)
            pygame.display.update()
        dt = clock.tick(40) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_SPACE:
                    if car_y == 750:
                        start = True
                        car_y_change = -20
                elif start:
                    if car_y <= y_start_position:
                        if event.key == pygame.K_LEFT:
                            car_x_change = -15
                        elif event.key == pygame.K_RIGHT:
                            car_x_change = 15
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
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
            for car in traffic_list:
                car.move(traffic_list)
                if not car.passed and car.y > car_y + 50:
                    score += 1
                    car.passed = True

        if score > high_score:
            high_score = score

        if car_x + car_x_change < 80:
            car_x = 80
        elif car_x + car_x_change > 480:
            car_x = 480
        else:
            car_x += car_x_change

        player_rect = pygame.Rect(car_x, car_y, car_image.get_width(), car_image.get_height())
        for car in traffic_list:
            traffic_rect = pygame.Rect(car.x, car.y, car.image.get_width(), car.image.get_height())
            if player_rect.colliderect(traffic_rect):
                quit_game = True
        
        background.draw()
        for car in traffic_list:
            car.draw()

        screen.blit(car_image, (car_x, car_y))
        
        if start:
            score_text = "Score: " + str(score)
            score_message(score_text, black)
            high_score_text = "High Score: " + str(high_score)
            high_score_message(high_score_text, black)


        pygame.display.update()
        clock.tick(40)

    save_high_score(high_score)
    
    screen.fill (black)
    death_message("You died, Press R to Play Again Or Q To Quit", white)
    pygame.display.update()



    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_r:
                    game_loop()


game_loop()
