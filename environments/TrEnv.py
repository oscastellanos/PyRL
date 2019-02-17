# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 15:54:28 2018

@author: Osvaldo Castellanos
"""

# !/usr/bin/env python
import os, pygame
import numpy as np
from pygame.locals import *
import sys

#sys.path.append('../')
#from example_support import ExampleAgent, ReplayMemory, loop_play_forever
#from base.pygamewrapper import PyGameWrapper

main_dir = os.path.split(os.path.abspath(__file__))[0]

MEAN = 30
STD = 10
CYCLE = 15

# Default Car drives horizontally
class Car():
    def __init__(self, location, height, speed, screen):
        self.stop = True
        self.counter = int(np.random.normal(MEAN, STD))
        self.no_collision = True
        self.speed = speed
        #pygame.sprite.Sprite.__init__(self)
        car = load_image('square.png').convert()
        self.image = pygame.transform.scale(car, (15, 10))
        self.screen = screen
        self.pos = self.image.get_rect().move(location, height)
        self.stationary = False
        self.velocity = 0
        self.waiting = 0

    def move(self):
        self.pos = self.pos.move(self.speed, 0)

    def position(self):
        return self.pos

    def stopping(self):
        self.stationary = True
        self.waiting += 1
        self.velocity = 0

    def resume_driving(self):
        self.stationary = False
        self.waiting = 0
        self.velocity = self.speed

    def draw(self):
        self.screen.blit(self.image, self.pos)

class CarVertical(Car):
    def __init__(self, location, height, speed, screen):
        Car.__init__(self, location, height, speed, screen)
        car = load_image('square-vertical.png').convert()
        self.image = pygame.transform.scale(car, (10, 15))

    def move(self):
        self.pos = self.pos.move(0, self.speed)

        # scree.blit(self.image_vertical)


class Lane():
    def __init__(self, screen):
        self.mean = 30
        self.std = 10
        self.cycle = 15
        self.vehicles_driving = []
        self.red_counter = 0
        self.count = 0
        self.num_of_cars = .90
        self.screen = screen

    def generateVehicles(self):
        pass

    def draw(self):
        pygame.display.update()
        #pygame.time.delay(50)

        # update the sprites in each class
        #self.car.draw(self.screen)
        for _ in self.vehicles_driving:
            _.draw()
class WestLane(Lane):
    def __init__(self, screen):
        Lane.__init__(self, screen)

    def populate(self):
        if np.random.rand() > self.num_of_cars:
            occupy = False
            for _ in self.vehicles_driving:
                if _.pos.left >= 615:
                    occupy = True
                    break
            if occupy == False:
                self.vehicles_driving.append(Car(600, 370, speed=-2, screen=screen))


class EastLane(Lane):
    def __init__(self, screen):
        Lane.__init__(self, screen)

    def generateVehicles(self):
        if np.random.rand() > self.num_of_cars:
            occupy = False
            for _ in self.vehicles_driving:
                if _.pos.left <= 17:
                    occupy = True
                    break
            if occupy == False:
                self.vehicles_driving.append(Car(0, 395, speed=2, screen=self.screen))

    def update(self, light):
        for o in self.vehicles_driving:
            #screen.blit(background, o.pos, o.pos)
            o.draw()
            if ((o.pos.right > 282) & (o.pos.right < 285) & ((light == 1) | (light == 2) | (light == 4))):
                continue
            else:
                collision = False

                for e in self.vehicles_driving:
                    if (o.pos.right + o.speed > e.pos.left) & (o.pos.right < e.pos.right):
                        collision = True
                        break
                if collision == False:
                    o.move()
            #screen.blit(o.image, o.pos)
            o.draw()
            if o.pos.left < 622:
                self.vehicles_driving.append(o)

class NorthLane(Lane):
    def __init__(self, screen):
        Lane.__init__(self, screen)

    def generateVehicles(self):
        if np.random.rand() > self.num_of_cars:
            occupy = False
            for _ in self.vehicles_driving:
                if _.pos.top <= 14:
                    occupy = True
                    break
            if occupy == False:
                self.vehicles_driving.append(CarVertical(325, 743, speed=-2, screen=screen))

class SouthLane(Lane):
    def __init__(self, screen):
        Lane.__init__(self, screen)

    def generateVehicles(self):
        if np.random.rand() > self.num_of_cars:
            occupy = False
            for _ in self.vehicles_driving:
                if _.pos.top <= 14:
                    occupy = True
                    break
            if occupy == False:
                self.vehicles_driving.append(CarVertical(295, 0, speed=2, screen=screen))

class TrafficSignal:
    def __init__(self, screen):
        self.light = 0
        self.red_light = load_image('red_horizontal.jpg').convert()
        self.rv = load_image('red_v.jpg').convert()
        self.green_light = load_image('green_horizontal.jpg').convert()
        self.gv = load_image('green_v.jpg').convert()
        yellow_light = load_image('yellow_traffic_light.png').convert()
        yv = load_image('yellow_traffic_light_v.png').convert()
        self.yellow_light = pygame.transform.scale(yellow_light, (75, 30))
        self.yv = pygame.transform.scale(yv, (30, 75))
        self.screen = screen
        self.north = NorthLane(self.screen)
        self.south = SouthLane(self.screen)
        self.east = EastLane(self.screen)
        self.west = WestLane(self.screen)

    def sequence(self):
        if self.light == 0:
            self.light = 2
        elif self.light == 2:
            self.light = 1
        elif self.light == 1:
            self.light = 4
        elif self.light == 4:
            self.light = 0

    def act(self, action):
        if action == 0:
            self.light = 0
        elif action == 1:
            self.light = 1
        elif action == 2:
            self.light = 2
        elif action == 4:
            self.light = 4

    def currentSignal(self):
        return self.light

    # previously was blit_light
    def draw(self):
        if self.light == 1:
            self.screen.blit(self.red_light, (350, 330))
            self.screen.blit(self.gv, (245, 285))
        elif self.light == 2:
            self.screen.blit(self.yellow_light, (350, 330))
            self.screen.blit(self.rv, (245, 285))
        elif self.light == 0:
            self.screen.blit(self.green_light, (350, 330))
            self.screen.blit(self.rv, (245, 285))
        elif self.light == 4:
            self.screen.blit(self.red_light, (350, 330))
            self.screen.blit(self.yv, (245, 285))

    def step(self):
        self.east.generateVehicles()
        self.east.update(self.currentSignal())
        self.east.draw()
        self.draw()




# TrafficSimulator is the container and controller class. Its constructor makes and embeds
# instances of the car, traffic signal, and lane classes.
class TrafficSimulator:
    def __init__(self, width=622, height=743):
        self.actions = {
            "left": K_LEFT, # red
            "right": K_RIGHT, #green
            "up": K_UP, #yellow_green
            "down": K_DOWN  #yellow_red
        }
        self.reward_sum = 0.0
        self.collision = False
        #PyGameWrapper.__init__(self, width, height, actions=actions)
        self.screen = pygame.display.set_mode((width, height))
        self.background = load_image('road-with-lanes2.png').convert()
        self.action = 0
        self.count = 0
        self.num_of_cars = .98
        self.signal_controller = TrafficSignal(self.screen)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.signal_controller.draw()

    def getGameState(self):
        pass

    def getReward(self):
        return self.reward_sum

    def game_over(self):
        # pong used 11 as max score
        return (self.collision == True)

    def init(self):
        pass

    def reset(self):
        self.init()

    def _handle_player_events(self):
        for event in pygame.event.get():
            #if event.type in (QUIT, KEYDOWN):
            #    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                key = event.key

                if key == self.actions["left"]:
                    self.action = 1

                if key == self.actions["right"]:
                    self.action = 0

                if key == self.actions["up"]:
                    self.action = 2

                if key == self.actions["down"]:
                    self.action = 4

    def step(self):
        #dt /= 1000.0
        self._handle_player_events()
        self.signal_controller.act(self.action)
        self.draw()
        self.signal_controller.step()
        self.signal_controller.draw()


# quick function to load an image
def load_image(name):
    path = os.path.join(main_dir, 'Traffic_data', name)
    return pygame.image.load(path).convert()

def traffic_signal(red_time, green_time, yellow_time):
    while True:
        for _ in range(green_time):
            yield 0
        for _ in range(yellow_time):
            yield 2
        for _ in range(red_time):
            yield 1
        for _ in range(yellow_time):
            yield 4

def debug(count, traffic_obj, traffic_obj_vertical):
    print("Count: " + str(count))
    print("Horizontal:  " + str(traffic_obj) + "  Vertical:  " + str(traffic_obj_vertical))



if __name__ == '__main__':
    pygame.init()
    game = TrafficSimulator(width=622, height=743)
    #game.screen = pygame.display.set_mode(game.getScreenDims(), 0, 32)
    game.clock = pygame.time.Clock()
    game.rng = np.random.RandomState(24)
    game.init()

    while True:
        #if game.game_over():
        #    game.init()

        #dt = game.clock.tick_busy_loop(30)
        game.step()
        pygame.display.update()