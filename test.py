from Settings import *
import pyglet
from math import cos, sin, radians, sqrt, fabs

class Ship(pyglet.sprite.Sprite):

    def __init__(self, img, x, y):
        image = pyglet.resource.image(img)
        image.anchor_x = image.width / 2
        image.anchor_y = image.height / 3
        super().__init__(image, x, y)
        self.scale = SHIP_SCALE
        self.speed = [0, 0, 0]

    def control(self, dt):
        if self.keyup:
            self.speed[1] += self.maxforce[0] * dt * cos(radians(self.rotation)) / self.mass[0]
            self.speed[0] += self.maxforce[0] * dt * sin(radians(self.rotation)) / self.mass[0]
        if self.keydown:
            self.speed[1] -= self.maxforce[0] * dt * cos(radians(self.rotation)) / self.mass[0]
            self.speed[0] -= self.maxforce[0] * dt * sin(radians(self.rotation)) / self.mass[0]
        if self.keyright:
            self.speed[2] += self.maxforce[1] * dt / self.mass[1]
        if self.keyleft:
            self.speed[2] -= self.maxforce[1] * dt / self.mass[1]

    def physics(self, dt):
        self.speed[0] *= (1 - (SLOW * dt / self.mass[0]))
        self.speed[1] *= (1 - (SLOW * dt / self.mass[0]))
        self.speed[2] *= (1 - (SLOW * dt / self.mass[1]))
        if self.keystop:
            fullstop = 0
            for i in range(3):
                if -RIFT < self.speed[i] < RIFT:
                    fullstop += 1
            if fullstop == 3:
                self.speed = [0, 0, 0]
            else:
                self.speed[2] *= (1 - 2 * dt)

    def force(self, fx, fy, m, dt):
        self.speed[0] += dt * fx / self.mass[0]
        self.speed[1] += dt * fy / self.mass[0]
        self.speed[2] += dt * m / self.mass[1]

    def update(self, dt):
        self.physics(dt)
        self.control(dt)
        self.x += self.speed[0] * dt
        self.y += self.speed[1] * dt
        self.rotation += self.speed[2] * dt

    def set(self, physics, engine):
        self.mass = physics
        self.maxforce = engine

    def drawstats(self):
        stats = "speed: " + str(self.speed[0]) + " | " + str(self.speed[1]) + " | " +  str(self.speed[2])
        stats_label = pyglet.text.Label(text=stats, x=20, y=10)
        stats_label.draw()

    mass = STANDART_PHYSICS
    maxforce = STANDART_ENGINE
    keyleft = False
    keyright = False
    keyup = False
    keydown =  False
    keystop = False

def distance(ship1, ship2):
    res = sqrt((ship1.x - ship2.x)*(ship1.x - ship2.x) + (ship1.y - ship2.y)*(ship1.y - ship2.y))
    l = distance.last
    distance.last = res
    return (res < l), sqrt((ship1.x - ship2.x)*(ship1.x - ship2.x) + (ship1.y - ship2.y)*(ship1.y - ship2.y))
distance.last = 0

def main():
    precos = []
    presin = []
    prea = []
    for i in range(26):
        a = i / 25 * 3.1415 * 2.0
        #prea.append(a)
        precos.append(cos(a))
        presin.append(sin(a))

    window = pyglet.window.Window(WIN_WIDTH, WIN_HEIGHT, style=WIN_STYLE, caption=WIN_CAPTION,
                                  fullscreen=WIN_FULLSCREEN)
    ship1 = Ship("Small_Fighter.png", 4 * WIN_WIDTH / 5, 4 * WIN_HEIGHT / 5)
    #ship1.set(SHIP1_PHYSICS, SHIP1_ENGINE)
    ship2 = Ship("Small_Fighter.png", WIN_WIDTH / 5, WIN_HEIGHT / 5)
    #ship2.set(SHIP2_PHYSICS, SHIP2_ENGINE)


    @window.event
    def on_draw():
        window.clear()
        if (SHOW_CIRCLES):
            pyglet.graphics.glClearColor(0, 0, 0, 1)
            pyglet.graphics.glClear(pyglet.graphics.GL_COLOR_BUFFER_BIT)
            pyglet.graphics.glColor3ub(0, 0,    55)
            pyglet.graphics.glBegin(pyglet.graphics.GL_TRIANGLE_FAN)
            pyglet.graphics.glVertex2f(ship2.x, ship2.y) # центр окружности
            for i in range(26):
                pyglet.graphics.glVertex2f(ship2.x - precos[i] * SHIP_RADIUS, ship2.y - presin[i] * SHIP_RADIUS )
            pyglet.graphics.glEnd()
            pyglet.graphics.glColor3ub(0, 55, 0)
            pyglet.graphics.glVertex2f(ship1.x, ship1.y)
            pyglet.graphics.glBegin(pyglet.graphics.GL_TRIANGLE_FAN)
            for i in range(26):
                pyglet.graphics.glVertex2f(ship1.x - precos[i] * SHIP_RADIUS, ship1.y - presin[i] * SHIP_RADIUS)
            pyglet.graphics.glEnd()

        ship1.draw()
        ship2.draw()
        ship1.drawstats()

    @window.event
    def on_key_press(symbol, mod):
        if symbol == pyglet.window.key.LEFT:
            ship1.keyleft = True
        elif symbol == pyglet.window.key.RIGHT:
            ship1.keyright = True
        elif symbol == pyglet.window.key.UP:
            ship1.keyup = True
        elif symbol == pyglet.window.key.DOWN:
            ship1.keydown = True
        elif symbol == pyglet.window.key.SPACE:
            ship1.x = 4 * WIN_WIDTH / 5
            ship1.y = 4 * WIN_HEIGHT / 5
        elif symbol == pyglet.window.key.ROPTION:
            ship1.keystop = True
        elif symbol == pyglet.window.key.Q:
            ship2.keystop = True
        elif symbol == pyglet.window.key.A:
            ship2.keyleft = True
        elif symbol == pyglet.window.key.D:
            ship2.keyright = True
        elif symbol == pyglet.window.key.W:
            ship2.keyup = True
        elif symbol == pyglet.window.key.S:
            ship2.keydown = True
        elif symbol == pyglet.window.key.R:
            ship2.x = WIN_WIDTH / 5
            ship2.y = WIN_HEIGHT / 5

    @window.event()
    def on_key_release(symbol, mod):
        if symbol == pyglet.window.key.LEFT:
            ship1.keyleft = False
        elif symbol == pyglet.window.key.RIGHT:
            ship1.keyright = False
        elif symbol == pyglet.window.key.UP:
            ship1.keyup = False
        elif symbol == pyglet.window.key.DOWN:
            ship1.keydown = False
        elif symbol == pyglet.window.key.ROPTION:
            ship1.keystop = False
        elif symbol == pyglet.window.key.Q:
            ship2.keystop = False
        elif symbol == pyglet.window.key.A:
            ship2.keyleft = False
        elif symbol == pyglet.window.key.D:
            ship2.keyright = False
        elif symbol == pyglet.window.key.W:
            ship2.keyup = False
        elif symbol == pyglet.window.key.S:
            ship2.keydown = False

    def update(dt):
        ship1.update(dt)
        ship2.update(dt)
        #ship1.x = WIN_WIDTH / 2
        #ship1.y = WIN_HEIGHT / 2
        #ship1.speed[0] = ship1.speed[1] = 0
        if PHYSICS_MODE:
            con, dist = distance(ship1, ship2)
            cosA = (ship1.x - ship2.x) / dist
            sinA = (ship1.y - ship2.y) / dist
            if (PHYSICS_MODE == 1 and 0 < dist < 2 * SHIP_RADIUS and (con or MATERIAL)):
                dl = 2 * SHIP_RADIUS - dist
                force = ELASTICITY * min(dl, MAX_DL)
                turn = (ship2.speed[1] - ship1.speed[1]) * cosA + (ship1.speed[0]- ship2.speed[0]) * sinA  - radians(ship1.speed[2] + ship2.speed[2]) * dist/2
                friction = force * COEFFICIENT + fabs(turn) * ROUGHNESS
                maxm = friction * dist / 2
                if (turn > 0):
                    ship1.force(force * cosA - friction * sinA, force * sinA + friction * cosA, maxm, dt)
                    ship2.force(-force * cosA + friction * sinA, -force * sinA - friction * cosA, maxm, dt)
                else:
                    ship1.force(force * cosA + friction * sinA, force * sinA - friction * cosA, -maxm, dt)
                    ship2.force(-force * cosA - friction * sinA, -force * sinA + friction * cosA, -maxm, dt)
            elif (PHYSICS_MODE == 2):
                vector = (ship1.x - ship2.x, ship1.y - ship2.y) #from ship1 to ship2
                impulse = (ship1.speed[0] * ship1.mass[0] + ship2.speed[0] * ship2.mass[0]) * cosA \
                          + (ship1.speed[1] * ship1.mass[0] + ship2.speed[1] * ship2.mass[0]) * sinA


    pyglet.clock.schedule_interval(update, 1 / UPDATE)

    pyglet.app.run()



if __name__ == "__main__":
    main()