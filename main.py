import arcade
from random import randint

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Studies game"


class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Menu Screen", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to F2 for new game.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game = GameView()
        self.window.show_view(game)


class Score(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.score_top = 0
        self.score_bottom = 0

    def draw(self, **kwargs):
        arcade.draw_text(f'{self.score_top} : {self.score_bottom}',
                         0, SCREEN_HEIGHT / 2 - 42, arcade.color.BLUE,
                         120,
                         font_name="a_LCDNova",
                         width=SCREEN_WIDTH,
                         align="center")


class Gates(arcade.Sprite):
    def __init__(self, **kwargs):
        super().__init__('gates.png', .50, **kwargs)


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
    timer = 0

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.score = Score()
        self.up_gates = Gates(angle=180.0)
        self.down_gates = Gates()
        self.bar = Bar()
        self.top_bar = Bar()
        self.ball = Ball()
        self.setup()

    def setup(self):

        self.down_gates.center_x = SCREEN_WIDTH / 2
        self.down_gates.center_y = SCREEN_HEIGHT / 8
        self.up_gates.center_x = SCREEN_WIDTH / 2
        self.up_gates.center_y = SCREEN_HEIGHT / 8 * 7

        self.bar.center_x = SCREEN_WIDTH / 2
        self.bar.center_y = SCREEN_HEIGHT / 5

        self.top_bar.center_x = SCREEN_WIDTH / 2
        self.top_bar.center_y = SCREEN_HEIGHT / 5 * 4

        self.ball.center_x = self.bar.center_x
        self.ball.bottom = self.bar.top
        self.ball.change_y = 0
        self.ball.change_x = self.bar.change_x

        self.bar.ball = True
        self.top_bar.ball = False
        self.score.score_top = 0
        self.score.score_bottom = 0
        self.timer = 10.0

    def on_draw(self):
        self.clear((217, 235, 246))
        self.score.draw()
        self.bar.draw()
        self.top_bar.draw()
        self.ball.draw()
        self.up_gates.draw()
        self.down_gates.draw()

        output = "{:02d}:{:02d}".format(int(self.timer // 60), int(self.timer % 60))
        arcade.draw_text(output, 0, 0, arcade.color.BLUE, 30, font_name="a_LCDNova")

    def update(self, delta_time: float):
        def autopilot(ball, bar, gate, stage=0):
            if stage == 0:
                if bar.left < gate.left or bar.right > gate.right:
                    bar.change_x = -bar.change_x
                elif bar.change_x == 0:
                    bar.change_x = -3

            if bar.ball:
                ball.change_x = bar.change_x
                ball.center_x = bar.center_x

        def check_gates(ball, gates, side=True):
            # шайба с права
            if side:
                if gates.right <= ball.center_x and gates.top > ball.center_y > gates.bottom:
                    ball.change_x = randint(2, 6)
            else:
                if gates.right <= ball.center_x and gates.bottom < ball.center_y < gates.top:
                    ball.change_x = randint(2, 6)

            # шайба с лева
            if side:
                if gates.left >= ball.center_x and gates.top > ball.center_y > gates.bottom:
                    ball.change_x = randint(-6, -2)
            else:
                if gates.left >= ball.center_x and gates.bottom < ball.center_y < gates.top:
                    ball.change_x = randint(-6, -2)

            # шайба сзади
            if side:
                if gates.bottom > ball.center_y and gates.left < ball.center_x < gates.right:
                    ball.change_y = -ball.change_y
            else:
                if gates.top < ball.center_y and gates.left < ball.center_x < gates.right:
                    ball.change_y = -ball.change_y

            # Г-О-О-О-Л
            if side:
                if gates.right > ball.right and gates.bottom < ball.bottom and \
                        gates.top > ball.top and gates.left < ball.left and ball.change_y < 0:
                    self.score.score_top += 1
                    ball.bottom = self.bar.top
                    ball.center_x = self.bar.center_x
                    self.bar.ball = True
                    ball.change_y = 0
                    ball.change_x = self.bar.change_x
            else:
                if gates.right > ball.right and gates.bottom > ball.bottom and \
                        gates.top > ball.top and gates.left < ball.left and ball.change_y > 0:
                    self.score.score_bottom += 1
                    ball.top = self.top_bar.bottom
                    ball.center_x = self.bar.center_x
                    self.top_bar.ball = True
                    ball.change_y = 0
                    ball.change_x = self.top_bar.change_x
        self.timer -= delta_time
        self.timer = max(self.timer, 0)
        if arcade.check_for_collision(self.ball, self.bar):
            self.ball.change_y = -self.ball.change_y
            self.ball.change_x += self.bar.change_x // 2

        if arcade.check_for_collision(self.ball, self.top_bar):
            self.ball.change_y = -self.ball.change_y
            self.ball.change_x += self.bar.change_x // 2

        if arcade.check_for_collision(self.ball, self.down_gates):
            check_gates(self.ball, self.down_gates, side=True)

        if arcade.check_for_collision(self.ball, self.up_gates):
            check_gates(self.ball, self.up_gates, side=False)

        autopilot(self.ball, self.top_bar, self.up_gates)
        self.ball.update()
        self.bar.update()
        self.top_bar.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()
        if symbol == arcade.key.F2:
            self.setup()
        if self.timer > 0:
            if symbol == arcade.key.RIGHT:
                self.bar.change_x = 3
            if symbol == arcade.key.LEFT:
                self.bar.change_x = -3
            if symbol == arcade.key.SPACE:
                if self.bar.ball:
                    self.bar.ball = False
                    self.ball.change_y = 6
                    self.ball.change_x = randint(-7, 7)
                if self.top_bar.ball:
                    self.top_bar.ball = False
                    self.ball.change_y = -6
                    self.ball.change_x = randint(-7, 7)

        if self.bar.ball:
            self.ball.change_x = self.bar.change_x
        if self.top_bar.ball:
            self.ball.change_x = self.top_bar.change_x

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in [arcade.key.RIGHT, arcade.key.LEFT]:
            self.bar.change_x = 0
        if self.bar.ball:
            self.ball.change_x = self.bar.change_x


if __name__ == '__main__':
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu = MenuView()
    arcade.run()
