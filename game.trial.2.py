import pyxel
import random

class App:
    def __init__(self):
        pyxel.init(160, 120, caption="Fortune Ball Catch Game")
        pyxel.load("assets/fbcg.pyxres")
        self.ball_x = [random.randint(0, 136) for i in range(5)]
        self.ball_y = [random.randint(0, 40) for i in range(5)]
        self.ball_speed = [random.randint(1, 3) for i in range(5)]
        self.catch_x = 72
        self.catch_y = 100
        self.catch_width = 16
        self.catch_height = 8
        self.catch_score = 0
        self.catch_time = 0
        self.fortune = "Excellent Luck"
        self.fortune_count = 0
        self.fortune_text = ""
        self.game_state = "fortune"
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_state == "fortune":
            if pyxel.btnp(pyxel.KEY_Y):
                self.fortune_count += 1
            elif pyxel.btnp(pyxel.KEY_N):
                self.fortune_count = 0
            if self.fortune_count >= 5:
                self.fortune = "Excellent Luck"
            elif self.fortune_count >= 3:
                self.fortune = "Good Luck"
            elif self.fortune_count >= 1:
                self.fortune = "Small Luck"
            else:
                self.fortune = "Minor Luck"
            self.fortune_text = "Your fortune is " + self.fortune
            self.game_state = "catch"
        elif self.game_state == "catch":
            if pyxel.btn(pyxel.KEY_LEFT):
                self.catch_x -= 2
            elif pyxel.btn(pyxel.KEY_RIGHT):
                self.catch_x += 2
            if self.catch_x < 0:
                self.catch_x = 0
            elif self.catch_x > 144:
                self.catch_x = 144
            self.catch_time += 1
            if self.catch_time >= 600:
                self.game_state = "end"
            for i in range(5):
                self.ball_y[i] += self.ball_speed[i]
                if self.ball_y[i] > 120:
                    self.ball_x[i] = random.randint(0, 136)
                    self.ball_y[i] = random.randint(0, 40)
                    self.ball_speed[i] = random.randint(1, 3)
                if (self.ball_x[i] + 8 > self.catch_x and self.ball_x[i] < self.catch_x + self.catch_width and
                        self.ball_y[i] + 8 > self.catch_y and self.ball_y[i] < self.catch_y + self.catch_height):
                    self.catch_score += 1
                    self.ball_x[i] = random.randint(0, 136)
                    self.ball_y[i] = random.randint(0, 40)
                    self.ball_speed[i] = random.randint(1, 3)
            if self.catch_score >= 5:
                self.fortune_text = "Your fortune is Super Luck"
                self.game_state = "end"
            elif self.catch_time >= 600:
                self.game_state = "end"

    def draw(self):
        pyxel.cls(0)
        if self.game_state == "fortune":
            pyxel.text(20, 50, "Answer the question with Y or N", 7)
            pyxel.text(20, 60, "Yes: Excellent Luck", 7)
            pyxel.text(20, 70, "No: