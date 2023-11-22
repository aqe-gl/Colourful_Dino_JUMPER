import arcade
import random

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
SCREEN_TITLE = 'No Internet'
GRAVITATION = 0.5
FLOOR = 35 * SCREEN_HEIGHT / 100
DINO_HEIGHT = 20
CACTUS_SPEED = 20


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        self.bg = arcade.load_texture('images/bg.png')
        self.dino = Dino('images/dino1.png', scale=1.8)
        self.cactus = Cactus('images/cactus1.png', scale=1.8)
        self.game_over = arcade.load_texture('images/game_over.png')
        self.game = True

    def setup(self):
        self.dino.center_x = 25 * SCREEN_WIDTH / 100
        self.dino.center_y = FLOOR
        self.dino.append_texture(arcade.load_texture('images/dino2.png'))
        self.dino.append_texture(arcade.load_texture('images/dino3.png'))
        self.cactus.center_x = SCREEN_WIDTH
        self.cactus.center_y = FLOOR
        self.cactus.append_texture(arcade.load_texture('images/cactus2.png'))
        self.cactus.change_x = CACTUS_SPEED

    def on_draw(self):
        self.clear((255, 255, 255))
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg)
        self.dino.draw()
        self.cactus.draw()
        if not self.game:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT,
                                          self.game_over)
        arcade.draw_text(f'score: {self.cactus.score}', SCREEN_WIDTH - 120, SCREEN_HEIGHT - 40, (255, 255, 255), font_size=20)
        if self.cactus.score == 20:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.load_texture('images/win.png'))


    def update(self, delta_time: float):
        if self.game:
            self.dino.update_animation(delta_time)
            self.dino.update()
            self.cactus.update_animation(delta_time)
            self.cactus.update()
            if arcade.check_for_collision(self.dino, self.cactus):
                self.game = False

    def on_resize(self, width: float, height: float):
        print('test')
        self.on_draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if self.game:
            if symbol == arcade.key.SPACE and not self.dino.jump:
                self.dino.change_y = DINO_HEIGHT
                self.dino.jump = True


class Animate(arcade.Sprite):
    i = 0
    time = 0

    def update_animation(self, delta_time: float = 1 / 60):
        self.time += delta_time
        if self.time >= 0.1:
            self.time = 0
            if self.i == len(self.textures) - 1:
                self.i = 0
            else:
                self.i += 1
            self.set_texture(self.i)


class Dino(Animate):
    jump = False

    def update(self):
        self.center_y += self.change_y
        self.change_y -= GRAVITATION
        if self.center_y < FLOOR:
            self.center_y = FLOOR
            self.jump = False


class Cactus(Animate):
    score = 0

    def update(self):
        self.center_x -= self.change_x
        if self.right < 0:
            self.left = SCREEN_WIDTH + random.randint(0, SCREEN_WIDTH)
            self.score += 1


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()

arcade.run()
