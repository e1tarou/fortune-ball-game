import pyxel
import random
import math

class FortuneGame:
    def __init__(self):
        # ゲームの状態
        self.questions = [
            "Is today your lucky day? Yes or No",
            "Did you have your meal? Yes or No",
            "Have you finished your homework? Yes or No",
            "Are you feeling well? Yes or No",
            "Did you smile today? Yes or No"
        ]
        self.current_question_index = 0
        self.yes_count = 0
        self.no_count = 0
        self.fortune = ""
        self.game_over = False
        self.answered = False

    def update(self):
        if not self.game_over and not self.answered:
            current_question = self.questions[self.current_question_index]

            if pyxel.btnp(pyxel.KEY_Y):
                self.yes_count += 1
                self.answered = True
            elif pyxel.btnp(pyxel.KEY_N):
                self.no_count += 1
                self.answered = True

            if self.answered:
                self.current_question_index += 1
                self.answered = False

                # Check if all questions have been asked
                if self.current_question_index >= len(self.questions):
                    self.calculate_fortune()
                    self.game_over = True

    def draw(self):
        # 画面クリア
        pyxel.cls(0)

        # 質問の表示
        current_question = self.questions[self.current_question_index]
        pyxel.text(10, 50, current_question, pyxel.COLOR_WHITE)

        # YesとNoの回数の表示
        pyxel.text(10, 60, "Yes (Y Key): {}".format(self.yes_count), pyxel.COLOR_GREEN)
        pyxel.text(10, 70, "No (N Key): {}".format(self.no_count), pyxel.COLOR_RED)

        # 運勢の表示
        if self.fortune:
            pyxel.text(40, 90, "Your Fortune: {}".format(self.fortune), pyxel.COLOR_WHITE)
            pyxel.text(40, 100, "Press 'Enter' to continue", pyxel.COLOR_WHITE)

    def calculate_fortune(self):
        total_count = self.yes_count + self.no_count

        if total_count == 0:
            self.fortune = "Excellent Luck"
        elif self.yes_count / total_count >= 0.8:
            self.fortune = "Excellent Luck"
        elif self.yes_count / total_count >= 0.6:
            self.fortune = "Good Luck"
        elif self.yes_count / total_count >= 0.4:
            self.fortune = "Small Luck"
        else:
            self.fortune = "Minor Luck"

class BallCatchGame:
    def __init__(self):
        # ゲームの状態
        self.player_x = 75
        self.ball_x = random.randint(0, 160)
        self.ball_y = 0
        self.ball_speed = 4
        self.ball_angle = random.uniform(math.pi / 4, math.pi / 2)  # Random angle between pi/4 and pi/2
        self.game_over = False
        self.super_luck = False
        self.end_message = ""
        self.timer = 600  # 10秒

    def update(self):
        if not self.game_over:
            # ボールの移動
            self.ball_x += self.ball_speed * math.cos(self.ball_angle)
            self.ball_y += self.ball_speed * math.sin(self.ball_angle)

            # ボールが画面外に出たら新しいボールを生成
            if self.ball_y > 120:
                self.ball_x = random.randint(0, 160)
                self.ball_y = 0
                self.ball_angle = random.uniform(math.pi / 4, math.pi / 2)

            # ボールがプレイヤーにキャッチされたか判定
            if (
                self.ball_x + 4 > self.player_x
                and self.ball_x < self.player_x + 20
                and self.ball_y + 4 > 110
                and self.ball_y < 120
            ):
                if random.random() < 0.1:
                    self.super_luck = True
                self.game_over = True

            # マウス移動時の処理
            self.player_x = max(0, min(140, pyxel.mouse_x - 10))

            # タイマーの更新
            self.timer -= 1
            if self.timer <= 0:
                self.game_over = True

    def draw(self):
        # 画面クリア
        pyxel.cls(0)

        # プレイヤーの描画
        pyxel.rect(self.player_x, 110, 20, 10, pyxel.COLOR_WHITE)

        # ボールの描画
        pyxel.circ(self.ball_x + 2, self.ball_y + 2, 2, pyxel.COLOR_YELLOW)

        # ゲームオーバー画面の表示
        if self.game_over:
            if self.super_luck:
                pyxel.text(45, 50, "Super Luck!", pyxel.COLOR_WHITE)
            else:
                pyxel.text(45, 60, "Good Luck", pyxel.COLOR_WHITE)

    def on_mouse_motion(self, x, y, dx, dy):
        pass

class FortuneBallCatchGame:
    def __init__(self):
        # 占いゲームの初期化
        self.fortune_game = FortuneGame()

        # ボールキャッチゲームの初期化
        self.ball_catch_game = BallCatchGame()

        # ゲームの状態
        self.current_game = self.fortune_game

        # イベント登録
        pyxel.init(160, 120, "Fortune Ball Catch Game")
        pyxel.mouse(True)  # Show the mouse cursor
        pyxel.run(self.update, self.draw)

    def update(self):
        self.current_game.update()

        # 占いゲームが終了したらボールキャッチゲームに切り替える
        if self.current_game.game_over and isinstance(self.current_game, FortuneGame):
            self.current_game = self.ball_catch_game

    def draw(self):
        self.current_game.draw()

if __name__ == "__main__":
    FortuneBallCatchGame()


