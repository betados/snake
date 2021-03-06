""" Snake game for codeskulptor.org """

import simplegui
import random
import math


class Snake(object):

    def __init__(self, width):
        self.velMod = 1
        self.vel = {'x': self.velMod, 'y': 0}
        self.lista = [{'x': 2, 'y': 2}]
        self.width = width
        # self.add()
        self.keyDict = {37: self.left, 38: self.up, 39: self.right, 40: self.down}
        self.estado = None
        self.keyDict[39]()

    def add(self):
        self.lista.append({'x': self.lista[-1]['x'], 'y': self.lista[-1]['y']})

    def draw(self, canvas):
        for element in self.lista:
            Square((int(element['x']) * self.width, int(element['y']) * self.width),
                   self.width-4).draw(canvas)

    def actualize(self):
        for i in range(1, len(self.lista)):
            self.lista[-i] = dict(self.lista[-i-1])

        self.lista[0]['x'] += self.vel['x']
        self.lista[0]['y'] += self.vel['y']
        # TODO si se sale por un lado que vuelva por el otro

    def left(self):
        if self.estado != "right":
            self.vel = {'x': -self.velMod, 'y': 0}
            self.estado = "left"

    def right(self):
        if self.estado != "left":
            self.vel = {'x': self.velMod, 'y': 0}
            self.estado = "right"

    def up(self):
        if self.estado != "down":
            self.vel = {'x': 0, 'y': -self.velMod}
            self.estado = "up"

    def down(self):
        if self.estado != "up":
            self.vel = {'x': 0, 'y': self.velMod}
            self.estado = "down"


class Square(object):

    def __init__(self, pos, width, color='Blue'):
        self.color = color
        self.width = width
        self.lista = []
        self.pos(pos[0], pos[1])


    def draw(self, canvas):
        canvas.draw_polygon(self.lista, 1, self.color, self.color)

    def pos(self, x, y):
        self.lista = [(x, y), (x + self.width, y),
                      (x + self.width, y + self.width), (x, y + self.width)]


class Scenario(object):
    def __init__(self, width, height, res):
        self.width = width
        self.height = height
        self.res = res
        self.food = [(random.randrange(0, width/res), random.randrange(0, height/res)) for _ in range(3)]
        self.lightGreen = [Square((x+res*(y % (res*2) == 0), y), res, 'GreenYellow ') for x in range(width)
                           if x % (res*2) == 0 for y in range(height) if y % res == 0]
        self.backGround = Square((0, 0), width, 'DarkKhaki')

    def draw(self, canvas):
        self.backGround.draw(canvas)
        for square in self.lightGreen:
            square.draw(canvas)
        for apple in self.food:
            canvas.draw_circle(((apple[0]+0.5)*self.res, (apple[1]+0.5)*self.res), self.res/2 * 0.7, 1, 'Red', 'Red')

    def newApple(self):
        self.food.append((random.randrange(0, width/self.res), random.randrange(0, height/self.res)))


class Interaction(object):
    # TODO interaction snake-snake
    # @staticmethod
    def food(self, snake, scenario):
        food = list(scenario.food)
        for i, apple in enumerate(food):
            if snake.lista[0]['x'] == apple[0] and snake.lista[0]['y'] == apple[1]:
                snake.add()
                scenario.food.pop(i)
                scenario.newApple()
                break


# Handler for mouse click
def start():
    # Start the frame animation
    frame.start()
    timer = simplegui.create_timer(250, actualize)
    frame.set_keydown_handler(keyDown)
    timer.start()


def keyDown(key):
    print(key)
    try:
        snake.keyDict[key]()
    except:
        if key == 27:
            exit()

# Handler to draw on canvas
def draw(canvas):
    scenario.draw(canvas)
    snake.draw(canvas)

def actualize():
    snake.actualize()
    interaction.food(snake, scenario)


width = 320
height = 240
snake = Snake(20)
scenario = Scenario(width, height, 20)
interaction = Interaction()

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", width, height)
frame.add_button("Start", start)
frame.set_draw_handler(draw)
