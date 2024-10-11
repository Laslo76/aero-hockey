import arcade
from random import randint

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Studies game"


class Gates(arcade.Sprite):
    def __init__(self):
        super().__init__('gates.png', .50)


class Bar(arcade.Sprite):
    def __init__(self):
        super().__init__('bar.png', 1.0)
        self.ball = False

    def update(self):
        self.center_x += self.change_x
        if self.right >= SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
            self.change_x = 0
        if self.left <= 0:
            self.left = 0
            self.change_x = 0


class Ball(arcade.Sprite):
    def __init__(self):
        super().__init__('ball.png', 1.0)
        self.change_y = -6
        self.change_x = 6

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.bottom <= 0 or self.top >= SCREEN_HEIGHT:
            self.change_y = -self.change_y
        if self.left <= 0 or self.right >= SCREEN_WIDTH:
            self.change_x = -self.change_x


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.down_gates = Gates()
        self.bar = Bar()
        self.ball = Ball()
        self.setup()

    def setup(self):
        self.bar.center_x = SCREEN_WIDTH / 2
        self.bar.center_y = SCREEN_HEIGHT / 6
        self.ball.center_x = SCREEN_WIDTH / 2
        self.ball.center_y = SCREEN_HEIGHT * 7 / 8
        self.down_gates.center_x = SCREEN_WIDTH / 2
        self.down_gates.center_y = SCREEN_WIDTH / 7

    def on_draw(self):
        self.clear((217, 235, 246))
        self.bar.draw()
        self.ball.draw()
        self.down_gates.draw()

    def update(self, delta_time: float):
        if arcade.check_for_collision(self.ball, self.bar):
            self.ball.change_y = -self.ball.change_y
            self.ball.change_x += self.bar.change_x // 2
        if arcade.check_for_collision(self.ball, self.down_gates):
            # шайба с права
            if self.down_gates.right <= self.ball.center_x and self.down_gates.top > self.ball.center_y > self.down_gates.bottom:
                self.ball.change_x = randint(2, 6)
            # шайба с лева
            if self.down_gates.left >= self.ball.center_x and self.down_gates.top > self.ball.center_y > self.down_gates.bottom:
                self.ball.change_x = randint(-6, -2)
            # шайба сзади
            if self.down_gates.bottom > self.ball.center_y and self.down_gates.left < self.ball.center_x < self.down_gates.right:
                self.ball.change_x = -self.ball.change_x
                self.ball.change_y = -self.ball.change_y
            if self.down_gates.right > self.ball.right and \
                    self.down_gates.bottom < self.ball.bottom and \
                    self.down_gates.top > self.ball.top and\
                    self.down_gates.left < self.ball.left and self.ball.change_y < 0:
                print("ГООЛ")
                self.ball.bottom = self.bar.top
                self.ball.center_x = (self.bar.right + self.bar.left) / 2
                self.bar.ball = True
                self.ball.change_y = 0
                self.ball.change_x = self.bar.change_x

        self.ball.update()
        self.bar.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT:
            self.bar.change_x = 3
        if symbol == arcade.key.LEFT:
            self.bar.change_x = -3
        if symbol == arcade.key.SPACE:
            if self.bar.ball:
                self.bar.ball = False
                self.ball.change_y = -6
                self.ball.change_x = randint(-7, 7)

        if self.bar.ball:
            self.ball.change_x = self.bar.change_x

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in [arcade.key.RIGHT, arcade.key.LEFT]:
            self.bar.change_x = 0
        if self.bar.ball:
            self.ball.change_x = self.bar.change_x


if __name__ == '__main__':
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
