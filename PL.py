import tkinter as tk
import random
import os
import time
import platform
from tkinter import simpledialog

# =====================
# OS별 표시 설정
# =====================
USE_EMOJI = platform.system() == "Darwin"

# =====================
# 색상 설정
# =====================
COLOR_NORMAL = "#c49a6c"
COLOR_GOLD   = "#ffd700"
COLOR_BOMB   = "#ff6b6b"
COLOR_EMPTY  = "#f0f0f0"

# =====================
# 게임 설정
# =====================
GAME_TIME = 30
GRID_SIZE = 3
HOLE_COUNT = GRID_SIZE * GRID_SIZE

MIN_SPEED = 400
SPEED_DOWN = 100

RANK_FILE = "ranking.txt"
SOUND_DIR = "sounds"


class MoleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("두더지 잡기 게임")

        self.last_sound_time = 0
        self.sound_cooldown = 0.12

        self.player_name = self.ask_nickname()
        self.load_ranking()
        self.create_start_screen()

    # =====================
    # 효과음 재생
    # =====================
    def play_sound(self, filename):
        now = time.time()
        if now - self.last_sound_time < self.sound_cooldown:
            return

        path = os.path.join(SOUND_DIR, filename)
        if not os.path.exists(path):
            return

        system = platform.system()
        if system == "Darwin":
            os.system(f"afplay '{path}' &")
        elif system == "Windows":
            os.system(f'start "" "{path}"')
        elif system == "Linux":
            os.system(f'aplay "{path}" &')

        self.last_sound_time = now

    # =====================
    # 닉네임 입력
    # =====================
    def ask_nickname(self):
        name = simpledialog.askstring(
            "닉네임 설정",
            "닉네임을 입력하세요 (최대 8자):"
        )
        return name[:8] if name else "익명"

    # =====================
    # 시작 화면
    # =====================
    def create_start_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="🐹 두더지 잡기 게임 🐹",
                 font=("Arial", 20)).pack(pady=20)

        tk.Button(self.root, text="Easy", font=("Arial", 14),
                  command=lambda: self.start_game(1000, 1)).pack(pady=5)

        tk.Button(self.root, text="Hard", font=("Arial", 14),
                  command=lambda: self.start_game(700, 2)).pack(pady=5)

        tk.Label(self.root, text="🏆 TOP 5 랭킹",
                 font=("Arial", 14)).pack(pady=10)

        for i, (name, score) in enumerate(self.ranking):
            tk.Label(self.root,
                     text=f"{i+1}. {name} - {score}점",
                     font=("Arial", 12)).pack()

    # =====================
    # 게임 시작
    # =====================
    def start_game(self, speed, score_mul):
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.time_left = GAME_TIME
        self.speed = speed
        self.score_mul = score_mul

        self.current_mole = None
        self.current_type = None
        self.mole_hit = True
        self.prev_type = None

        self.clear_screen()
        self.create_game_ui()
        self.update_timer()
        self.spawn_mole()

    # =====================
    # 게임 UI
    # =====================
    def create_game_ui(self):
        info = tk.Frame(self.root)
        info.pack(pady=10)

        self.score_label = tk.Label(info, text="점수: 0", font=("Arial", 14))
        self.score_label.pack(side=tk.LEFT, padx=10)

        self.combo_label = tk.Label(info, text="콤보: 0", font=("Arial", 14))
        self.combo_label.pack(side=tk.LEFT, padx=10)

        self.time_label = tk.Label(info, text="시간: 30", font=("Arial", 14))
        self.time_label.pack(side=tk.RIGHT, padx=10)

        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack()

        self.buttons = []
        for i in range(HOLE_COUNT):
            btn = tk.Button(
                self.grid_frame,
                text=" ",
                width=6,
                height=3,
                font=("Arial", 28, "bold"),
                bg=COLOR_EMPTY,
                command=lambda idx=i: self.hit_mole(idx)
            )
            btn.grid(row=i // GRID_SIZE, column=i % GRID_SIZE, padx=5, pady=5)
            self.buttons.append(btn)

    # =====================
    # 두더지 생성 + 콤보 판정
    # =====================
    def spawn_mole(self):
        if not self.mole_hit and self.prev_type == "normal":
            self.combo = 0
            self.combo_label.config(text=f"콤보: {self.combo}")

        self.clear_mole()
        self.current_mole = random.randint(0, HOLE_COUNT - 1)

        r = random.random()
        if r < 0.7:
            self.current_type = "normal"
            text = "🐹" if USE_EMOJI else "M"
            color = COLOR_NORMAL
        elif r < 0.9:
            self.current_type = "gold"
            text = "⭐" if USE_EMOJI else "G"
            color = COLOR_GOLD
        else:
            self.current_type = "bomb"
            text = "💣" if USE_EMOJI else "X"
            color = COLOR_BOMB

        self.buttons[self.current_mole].config(text=text, bg=color)

        self.mole_hit = False
        self.prev_type = self.current_type

        self.root.after(self.speed, self.spawn_mole)

    # =====================
    # 클릭 처리
    # =====================
    def hit_mole(self, index):
        if index != self.current_mole:
            self.combo = 0
            self.combo_label.config(text=f"콤보: {self.combo}")
            self.play_sound("bomb.wav")
            return

        self.mole_hit = True

        if self.current_type == "bomb":
            self.score -= 5 * self.score_mul
            self.play_sound("bomb.wav")
        elif self.current_type == "gold":
            self.combo += 1
            self.score += (3 + self.combo // 3) * self.score_mul
            self.play_sound("gold.wav")
        else:
            self.combo += 1
            self.score += (1 + self.combo // 3) * self.score_mul
            self.play_sound("hit.wav")

        self.max_combo = max(self.max_combo, self.combo)
        self.score_label.config(text=f"점수: {self.score}")
        self.combo_label.config(text=f"콤보: {self.combo}")
        self.clear_mole()

    # =====================
    # 두더지 제거
    # =====================
    def clear_mole(self):
        for btn in self.buttons:
            btn.config(text=" ", bg=COLOR_EMPTY)
        self.current_mole = None

    # =====================
    # 타이머
    # =====================
    def update_timer(self):
        if self.time_left <= 0:
            self.end_game()
            return

        if self.time_left % 10 == 0 and self.speed > MIN_SPEED:
            self.speed -= SPEED_DOWN

        self.time_label.config(text=f"시간: {self.time_left}")
        self.time_left -= 1
        self.root.after(1000, self.update_timer)

    # =====================
    # 게임 종료 (TOP5 기준 신기록)
    # =====================
    def end_game(self):
        before = self.ranking.copy()
        self.update_ranking(self.player_name, self.score)

        is_new_record = (self.player_name, self.score) in self.ranking and \
                        (self.player_name, self.score) not in before

        self.play_sound("end.wav")
        self.clear_screen()

        tk.Label(self.root, text="⏰ 게임 종료!",
                 font=("Arial", 22)).pack(pady=10)

        if is_new_record:
            tk.Label(self.root, text="🎉 신기록 달성!",
                     font=("Arial", 18), fg="red").pack(pady=5)

        tk.Label(self.root,
                 text=f"{self.player_name} : {self.score}점",
                 font=("Arial", 16)).pack()

        tk.Label(self.root,
                 text=f"최대 콤보: {self.max_combo}",
                 font=("Arial", 14)).pack(pady=5)

        tk.Button(self.root, text="메인 메뉴로",
                  font=("Arial", 14),
                  command=self.create_start_screen).pack(pady=15)

    # =====================
    # 랭킹 관리
    # =====================
    def load_ranking(self):
        self.ranking = []
        if os.path.exists(RANK_FILE):
            with open(RANK_FILE, "r") as f:
                for line in f:
                    if "," in line:
                        name, score = line.strip().split(",")
                        self.ranking.append((name, int(score)))

    def update_ranking(self, name, score):
        self.ranking.append((name, score))
        self.ranking = sorted(
            self.ranking, key=lambda x: x[1], reverse=True)[:5]
        with open(RANK_FILE, "w") as f:
            for n, s in self.ranking:
                f.write(f"{n},{s}\n")

    # =====================
    # 화면 초기화
    # =====================
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    MoleGame(root)
    root.mainloop()
