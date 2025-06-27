import pygame
import time
import random

pygame.init()

# display 
screen = pygame.display.set_mode((650, 800))
game_icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("2D Car Racing Game")

# clock and fonts
clock = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf", 40)
death_font = pygame.font.Font("freesansbold.ttf", 80)
death_other_font = pygame.font.Font("freesansbold.ttf", 30)

# colors
white = (255, 255, 255)
black = (0, 0, 0)

# load images
car_image = pygame.image.load('player_car.png')
map_image = pygame.image.load('map.png')
map_image = pygame.transform.scale(map_image, (650, 800))
traffic_1_image = pygame.image.load('car_1.png')
traffic_2_image = pygame.image.load('car_2.png')
traffic_3_image = pygame.image.load('car_3.png')
traffic_4_image = pygame.image.load('car_4.png')
traffic_5_image = pygame.image.load('car_5.png')

# lane locations
lanes = [115, 280, 430]

# class for traffic
class Traffic:
    def __init__(self, lane, image, speed):
        self.image = image
        self.x = lane
        self.y = random.randint(-1500, -100) # spawns car offscreen
        self.speed = speed
        self.passed = False # if player has passed

    def draw(self):
        screen.blit(self.image, (self.x, self.y)) # draw the ar on screen

    def move(self, all_traffic):
        self.y += self.speed # moves traffic down
        # if the car goes past the bottom on the screen
        if self.y > 800:
            while True:
                new_y = random.randint(-1500, -100)
                new_x = random.choice(lanes)
                
                # check if the traffic is overlapping eachother
                is_overlapping = False 
                for car in all_traffic:
                    if car is not self and car.x == new_x and abs(car.y - new_y) < 150:
                        is_overlapping = True
                        break
                # only respawns if not overlapping
                if not is_overlapping:
                    self.x = new_x
                    self.y = new_y
                    self.passed = False
                    break
# genorates traffic 
def generate_traffic():
    traffic_list = []
    traffic_images = [traffic_1_image, traffic_2_image, traffic_3_image, traffic_4_image, traffic_5_image]
    speed = 4


    for _ in range(5): # creates 5 traffic cars
        while True:
            lane = random.choice(lanes)
            y = random.randint(-1500, -100)
            image = random.choice(traffic_images)

            # stops overlapping
            is_overlapping = False
            for car in traffic_list:
                if car.x == lane and abs(car.y - y) < 180:
                    is_overlapping = True
                    break

            if not is_overlapping:
                new_car = Traffic(lane, image, speed)
                new_car.y = y
                traffic_list.append(new_car)
                break

    return traffic_list


# class for moving background
class MovingBackground:
    def __init__(self, image, speed):
        self.image = image
        self.speed = speed
        # first map spawns onscreen and second map spawns above the screen
        self.map1 = 0 
        self.map2 = -screen.get_height() 

    def update(self):
        # moves background
        self.map1 += self.speed
        self.map2 += self.speed
        if self.map1 >= screen.get_height():
            self.map1 = -screen.get_height()
        if self.map2 >= screen.get_height():
            self.map2 = -screen.get_height()

    def draw(self):
        screen.blit(self.image, (0, self.map1))
        screen.blit(self.image, (0, self.map2))

# text settings and loading and saving high score
def start_message(msg, text_colour):
    txt = font.render(msg, True, text_colour)
    text_box = txt.get_rect(center=(325, 100))
    screen.blit(txt, text_box)

def load_high_score():
    # loads the high score from the file, if file does not exist then high score returns to 0
    try:
        with open("HI_score_Racing.txt", 'r') as hi_score_file:
            return int(hi_score_file.read())
    except:
        return 0 
    
def save_high_score(high_score):
    # saves high score the the file
    with open("HI_score_Racing.txt", 'w') as hi_score_file:
        hi_score_file.write(str(high_score))
        
def message(msg, text_colour, x, y, font_type):
    txt = font_type.render(msg, True, text_colour)
    text_box = txt.get_rect(center=(x, y))
    screen.blit(txt, text_box)


# game loop
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
        # FPS
        dt = clock.tick(40) / 1000 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_SPACE:
                    if car_y == 750: # stops player from pressing space when not in starting position
                        start = True
                        car_y_change = -20
                elif start: 
                    if car_y <= y_start_position: # player can move once space is pressed and car gets to starting position
                        if event.key == pygame.K_LEFT:
                            car_x_change = -15
                        elif event.key == pygame.K_RIGHT:
                            car_x_change = 15
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    car_x_change = 0

        # animation of car starting to drive onto the road
        if car_y > y_start_position:
            car_y += car_y_change
            if car_y <= y_start_position:
                car_y = y_start_position
                car_y_change = 0
                current_speed = initial_speed
                background.speed = current_speed
        else:
            background.update()

        # update traffic and increase score when passed
        if car_y == y_start_position:
            for car in traffic_list:
                car.move(traffic_list)
                if not car.passed and car.y > car_y + 50:
                    score += 1
                    car.passed = True
                    # increase background speed
                    current_speed += 1
                    background.speed = current_speed
                    # increase traffic speed
                    for traffic_car in traffic_list:
                        traffic_car.speed += 1

        # updates high score
        if score > high_score:
            high_score = score
            
        # stop car from moving past edge of the road (yellow line on the map)
        if car_x + car_x_change < 80:
            car_x = 80
        elif car_x + car_x_change > 480:
            car_x = 480
        else:
            car_x += car_x_change
            
        #  collision
        player_rect = pygame.Rect(car_x, car_y, car_image.get_width(), car_image.get_height())
        for car in traffic_list:
            traffic_rect = pygame.Rect(car.x, car.y, car.image.get_width(), car.image.get_height())
            if player_rect.colliderect(traffic_rect):
                quit_game = True

        background.draw()
            
        # displays start message if game has not started
        if not start:
            message("Press Space To Start", black, 325, 100, font)
        else:
            # draw traffic and car only when game has started
            for car in traffic_list:
                car.draw()
            screen.blit(car_image, (car_x, car_y))
            # loads score and high score once game is started
            message("Score: " + str(score), black, 120, 50, font)
            message("High Score: " + str(high_score), black, 500, 50, font)

        pygame.display.update()
        clock.tick(40) # limit to 40fps

    # saves high score and display death screen 
    save_high_score(high_score)
    screen.fill (black)
    message("You Died", white, 325, 300, death_font)
    message("your score was " + str(score) + " your high score is " + str(high_score), white, 325, 400, death_other_font_) 
    message("Press R to Play Again Or Q To Quit", white, 325, 440, death_other_font)
    pygame.display.update()


    # allows player to quit or restart after death
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
                    game_loop() # restarts game


game_loop()




