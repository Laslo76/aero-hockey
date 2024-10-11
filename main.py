import arcade

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Studies game"


class Gates(arcade.Sprite):
    def __init__(self):
        super().__init__('gool.png', .50)

class Bar(arcade.Sprite):
    def __init__(self):
        super().__init__('bar.png', 1.0)

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
        self.change_y = -5
        self.change_x = 5

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.bottom <=0 or self.top >=SCREEN_HEIGHT:
            self.change_y = -self.change_y
        if self.left <= 0 or self.right >= SCREEN_WIDTH:
            self.change_x = -self.change_x


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        #self.up_gates = Gates()
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
        if arcade.check_for_collision(self.ball, self.down_gates):
            pass
        self.ball.update()
        self.bar.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT:
            self.bar.change_x = 3
        if symbol == arcade.key.LEFT:
            self.bar.change_x = -3

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in [arcade.key.RIGHT, arcade.key.LEFT]:
            self.bar.change_x = 0


if __name__ == '__main__':
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
