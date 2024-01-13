import pyxel
import random

class FortuneBallCatchGame:
    def __init__(self):
        # 占いゲームの初期化
        self.fortune_game = FortuneGame()

        # ボールキャッチゲームの初期化
        self.ball_catch_game = BallCatchGame()

        # ゲームの状態
        self.current_game = self.fortune_game

        # イベント登録
        pyxel.run(self.update, self.draw)

    def update(self):
        self.current_game.update()

        # 占いゲームが終了したらボールキャッチゲームに切り替える
        if self.current_game.game_over and isinstance(self.current_game, FortuneGame):
            self.current_game = self.ball_catch_game

        # ボールキャッチゲームが終了したら再び占いゲームに切り替える
        elif self.current_game.game_over and isinstance(self.current_game, BallCatchGame):
            self.current_game = self.fortune_game

    def draw(self):
        self.current_game.draw()

class FortuneGame:
    def __init__(self):
        # 初期化
        pyxel.init(160, 120, caption="Fortune Ball Catch Game")
        pyxel.mouse(True)

        # ゲームの状態
        self.question = "Is today your lucky day? Yes or No"
        self.yes_count = 0
        self.no_count = 0
        self.fortune = ""

        # イベント登録
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.fortune:
            if pyxel.btnp(pyxel.KEY_Y):
                self.yes_count += 1
            elif pyxel.btnp(pyxel.KEY_N):
                self.no_count += 1

            if self.yes_count + self.no_count >= 5:
                self.calculate_fortune()

    def draw(self):
        # 画面クリア
        pyxel.cls(0)

        # 質問の表示
        pyxel.text(10, 50, self.question, pyxel.COLOR_WHITE)

        # YesとNoの回数の表示
        pyxel.text(10, 60, "Yes: {}".format(self.yes_count), pyxel.COLOR_GREEN)
        pyxel.text(10, 70, "No: {}".format(self.no_count), pyxel.COLOR_RED)

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
        # 初期化
        pyxel.init(160, 120, caption="Fortune Ball Catch Game")
        pyxel.mouse(True)

        # ゲームの状態
        self.player_x = 75
        self.ball_x = random.randint(0, 160)
        self.ball_y = 0
        self.ball_speed = 2
        self.game_over = False
        self.super_luck = False
        self.end_message = ""
        self.timer = 600  # 10秒

        # イベント登録
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.game_over:
            # ボールの移動
            self.ball_y += self.ball_speed

            # ボールが画面外に出たら新しいボールを生成
            if self.ball_y > 120:
                self.ball_x = random.randint(0, 160)
                self.ball_y = 0

            # ボールがプレイヤーにキャッチされたか判定
            if (
                self.ball_x + 4 > self.player_x
                and self.ball_x < self.player_x + 20
                and self.ball_y + 4 > 110
            ):
                if random.random() < 0.1:
                    self.super_luck = True
                    self.game_over = True
                else:
                    self.game_over = True

            # タイマーの更新
            self.timer -= 1
            if self.timer <= 0:
                self.end_message = "The End"
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
                pyxel.text(55, 50, self.end_message, pyxel.COLOR_WHITE)
                if not self.super_luck:
                    pyxel.text(45, 60, "Press 'R' to retry", pyxel.COLOR_WHITE)

    def on_mouse_motion(self, x, y, dx, dy):
        # マウス移動時の処理
        self.player_x = max(0, min(140, x - 10))

        # ゲームオーバー時に'R'キーで再起動
        if pyxel.btnp(pyxel.KEY_R) and self.game_over:
            self.__init__()

if __name__ == "__main__":
    FortuneBallCatch
