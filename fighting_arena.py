import tkinter as tk
from tkinter import messagebox, ttk
import random

from mythical_beasts import Dragon, Phoenix, Kraken


class ArenaApp:
    """The Driver Application managing GUI elements, turn updates, and the Endless Mode architecture."""

    def __init__(self, window_root: tk.Tk):
        self.root = window_root
        self.root.title("Mythical Beasts: Endless Survival Arena")
        self.root.geometry("750x680")

        # Color profile configurations
        self.bg_main = "#121214"
        self.bg_card = "#1a1a24"
        self.fg_light = "#e1e1e6"
        self.accent_blue = "#04d361"
        self.accent_red = "#f75151"
        self.accent_purp = "#bd93f9"

        self.root.configure(bg=self.bg_main)

        self.player_beast = None
        self.cpu_beast = None
        self.round_count = 0
        self.survival_score = 0

        self.player_choices = {
            "Inferno Dragon": Dragon,
            "Solar Phoenix": Phoenix,
            "Abyssal Kraken": Kraken
        }

        self.build_selection_ui()

    def build_selection_ui(self):
        """Initial choice menu presentation."""
        self.clear_screen()
        self.round_count = 0
        self.survival_score = 0

        title = tk.Label(self.root, text="ENDLESS ARENA LADDER", font=("Courier New", 22, "bold"), fg="#ffb86c",
                         bg=self.bg_main)
        title.pack(pady=40)

        instruction = tk.Label(self.root, text="Select your core fighter archetype. Survive as many waves as possible:",
                               font=("Arial", 11), fg=self.fg_light, bg=self.bg_main)
        instruction.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg=self.bg_main)
        btn_frame.pack(pady=30)

        for name, beast_class in self.player_choices.items():
            btn = tk.Button(
                btn_frame,
                text=name,
                font=("Arial", 11, "bold"),
                width=18,
                height=2,
                bg=self.bg_card,
                fg="#8ff0a4",
                command=lambda b_type=beast_class, b_name=name: self.start_ladder_mode(b_type, b_name)
            )
            btn.pack(side=tk.LEFT, padx=15)

    def start_ladder_mode(self, chosen_class, name: str):
        """Instantiates player baseline selection object records."""
        self.player_beast = chosen_class(name)
        self.spawn_next_enemy()
        self.build_arena_ui()

    def spawn_next_enemy(self):
        """Generates random dynamic targets scaled against historical win metrics."""
        self.round_count = 0
        self.survival_score += 1

        cpu_raw_name, cpu_class = random.choice(list(self.player_choices.items()))
        self.cpu_beast = cpu_class(f"Rival {cpu_raw_name}")

        # Difficulty Multiplier: Enemies get 20% stronger per wave passed
        if self.survival_score > 1:
            scale = 1.0 + (self.survival_score - 1) * 0.20
            self.cpu_beast.scale_difficulty(scale)

    def build_arena_ui(self):
        """Draws live active dashboards tracking dynamic property metrics."""
        self.clear_screen()

        # Upper dashboard monitors
        status_frame = tk.Frame(self.root, bg=self.bg_main)
        status_frame.pack(fill=tk.X, pady=10, padx=30)

        self.score_lbl = tk.Label(status_frame, text=f"WAVE: {self.survival_score}", font=("Courier New", 12, "bold"),
                                  fg="#ff79c6", bg=self.bg_main)
        self.score_lbl.pack(side=tk.LEFT)

        self.turn_lbl = tk.Label(status_frame, text="ROUND 1", font=("Courier New", 12, "bold"), fg="#f1fa8c",
                                 bg=self.bg_main)
        self.turn_lbl.pack(side=tk.RIGHT)

        display_frame = tk.Frame(self.root, bg=self.bg_main)
        display_frame.pack(fill=tk.X, padx=30, pady=5)

        # Player Status Card Design
        p_panel = tk.Frame(display_frame, bg=self.bg_card, bd=2, relief=tk.RIDGE, padx=15, pady=15)
        p_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        self.p_name_lbl = tk.Label(p_panel, text="", font=("Arial", 12, "bold"), fg=self.accent_blue, bg=self.bg_card)
        self.p_name_lbl.pack(anchor=tk.W)
        self.p_health = ttk.Progressbar(p_panel, orient=tk.HORIZONTAL, length=180, mode='determinate')
        self.p_health.pack(fill=tk.X, pady=4)

        # Visual metrics layout tracking passive charges
        tk.Label(p_panel, text="Ultimate Energy:", font=("Arial", 9), fg="#aaa", bg=self.bg_card).pack(anchor=tk.W)
        self.p_ult_bar = ttk.Progressbar(p_panel, orient=tk.HORIZONTAL, length=180, mode='determinate')
        self.p_ult_bar.pack(fill=tk.X, pady=2)

        self.p_stat_lbl = tk.Label(p_panel, text="", font=("Courier New", 9), fg=self.fg_light, bg=self.bg_card,
                                   justify=tk.LEFT)
        self.p_stat_lbl.pack(anchor=tk.W, pady=4)

        # Enemy Status Card Design
        c_panel = tk.Frame(display_frame, bg=self.bg_card, bd=2, relief=tk.RIDGE, padx=15, pady=15)
        c_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        self.c_name_lbl = tk.Label(c_panel, text="", font=("Arial", 12, "bold"), fg=self.accent_red, bg=self.bg_card)
        self.c_name_lbl.pack(anchor=tk.W)
        self.c_health = ttk.Progressbar(c_panel, orient=tk.HORIZONTAL, length=180, mode='determinate')
        self.c_health.pack(fill=tk.X, pady=4)

        tk.Label(c_panel, text="Ultimate Energy:", font=("Arial", 9), fg="#aaa", bg=self.bg_card).pack(anchor=tk.W)
        self.c_ult_bar = ttk.Progressbar(c_panel, orient=tk.HORIZONTAL, length=180, mode='determinate')
        self.c_ult_bar.pack(fill=tk.X, pady=2)

        self.c_stat_lbl = tk.Label(c_panel, text="", font=("Courier New", 9), fg=self.fg_light, bg=self.bg_card,
                                   justify=tk.LEFT)
        self.c_stat_lbl.pack(anchor=tk.W, pady=4)

        # Central Operational Text Window Frame
        self.log_box = tk.Text(self.root, height=14, width=85, font=("Courier New", 9), bg="#282a36", fg="#f8f8f2",
                               state=tk.DISABLED)
        self.log_box.pack(pady=10)

        # Controller Commands Row Interface
        self.controls_frame = tk.Frame(self.root, bg=self.bg_main)
        self.controls_frame.pack(pady=10)

        self.btn_strike = tk.Button(self.controls_frame, text="Basic Strike", width=15, font=("Arial", 10, "bold"),
                                    bg="#44475a", fg=self.fg_light, command=self.do_player_strike)
        self.btn_strike.grid(row=0, column=0, padx=10)

        self.btn_special = tk.Button(self.controls_frame, text="Special Power", width=15, font=("Arial", 10, "bold"),
                                     bg="#6272a4", fg=self.fg_light, command=self.do_player_special)
        self.btn_special.grid(row=0, column=1, padx=10)

        self.btn_ultimate = tk.Button(self.controls_frame, text="ULTIMATE", width=15, font=("Arial", 10, "bold"),
                                      bg=self.accent_purp, fg=self.fg_light, command=self.do_player_ultimate)
        self.btn_ultimate.grid(row=0, column=2, padx=10)

        self.advance_turn_count()
        self.update_displays()
        self.append_log(f"[SYSTEM] Wave {self.survival_score} deployed. Elemental advantages active.")

    def advance_turn_count(self):
        """Steps forward through the tracking registers."""
        self.round_count += 1
        self.turn_lbl.config(text=f"ROUND {self.round_count}")

    def update_displays(self):
        """Calculates dynamic widths and properties cleanly."""
        self.p_health['value'] = (self.player_beast.health / self.player_beast.max_health) * 100
        self.c_health['value'] = (self.cpu_beast.health / self.cpu_beast.max_health) * 100

        self.p_ult_bar['value'] = self.player_beast.ultimate_gauge
        self.c_ult_bar['value'] = self.cpu_beast.ultimate_gauge

        self.p_name_lbl.config(text=f"{self.player_beast.name} ({self.player_beast.element})")
        self.c_name_lbl.config(text=f"{self.cpu_beast.name} ({self.cpu_beast.element})")

        p_metrics = f"HP: {self.player_beast.health}/{self.player_beast.max_health}\nATK: {self.player_beast.attack_power}  SPD: {self.player_beast.speed}\nULTIMATE: {self.player_beast.ultimate_gauge}%"
        self.p_stat_lbl.config(text=p_metrics)

        c_metrics = f"HP: {self.cpu_beast.health}/{self.cpu_beast.max_health}\nATK: {self.cpu_beast.attack_power}  SPD: {self.cpu_beast.speed}\nULTIMATE: {self.cpu_beast.ultimate_gauge}%"
        self.c_stat_lbl.config(text=c_metrics)

        # Ultimate action locking parameters based on passive metrics
        if self.player_beast.ultimate_gauge >= 100:
            self.btn_ultimate.config(bg="#ff5555", fg="#ffffff", state=tk.NORMAL)
        else:
            self.btn_ultimate.config(bg="#2b2b36", fg="#666677", state=tk.DISABLED)

    def append_log(self, text: str):
        self.log_box.config(state=tk.NORMAL)
        self.log_box.insert(tk.END, f"[W{self.survival_score} R{self.round_count}] {text}\n\n")
        self.log_box.see(tk.END)
        self.log_box.config(state=tk.DISABLED)

    def do_player_strike(self):
        self.append_log(self.player_beast.basic_attack(self.cpu_beast))
        self.check_or_continue_battle()

    def do_player_special(self):
        self.append_log(self.player_beast.execute_special_ability(self.cpu_beast))
        self.check_or_continue_battle()

    def do_player_ultimate(self):
        self.append_log(self.player_beast.execute_ultimate_ability(self.cpu_beast))
        self.check_or_continue_battle()

    def check_or_continue_battle(self):
        """Coordinates endless survival ladder progression tracking loops."""
        self.update_displays()

        if self.cpu_beast.health <= 0:
            # Reward player by regenerating 35% health before the next battle layer loads
            heal_bonus = int(self.player_beast.max_health * 0.35)
            self.player_beast.recover_health(heal_bonus)
            messagebox.showinfo("WAVE CLEARED",
                                f"Defeated the target. Survival Bonus: Restored {heal_bonus} health. Preparing Wave {self.survival_score + 1}!")
            self.spawn_next_enemy()
            self.build_arena_ui()
            return

        self.toggle_buttons(state=tk.DISABLED)
        self.root.after(1000, self.execute_cpu_turn)

    def execute_cpu_turn(self):
        if self.player_beast.health <= 0:
            return

        # CPU priority calculation layer checking state markers
        if self.cpu_beast.ultimate_gauge >= 100:
            log = self.cpu_beast.execute_ultimate_ability(self.player_beast)
        elif random.random() < 0.40:
            log = self.cpu_beast.execute_special_ability(self.player_beast)
        else:
            log = self.cpu_beast.basic_attack(self.player_beast)

        self.append_log(f"[ENEMY TURN]\n{log}")

        if self.player_beast.health <= 0:
            self.update_displays()
            messagebox.showerror("COMBAT TERMINATED",
                                 f"Your champion collapsed. Waves Survived: {self.survival_score - 1}")
            self.build_selection_ui()
            return

        self.advance_turn_count()
        self.update_displays()
        self.toggle_buttons(state=tk.NORMAL)

    def toggle_buttons(self, state):
        self.btn_strike.config(state=state)
        self.btn_special.config(state=state)
        if self.player_beast.ultimate_gauge < 100 and state == tk.NORMAL:
            pass
        else:
            self.btn_ultimate.config(state=state)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ArenaApp(root)
    root.mainloop()

