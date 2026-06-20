
import random
from mythical_beasts import Dragon, Phoenix, Kraken, Griffin

# --------------------------
# COLOR SETUP
# --------------------------
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"

BESTIARY = [Dragon, Phoenix, Kraken, Griffin]

RANK_TITLES = {
    0: "Arena Sweepings",
    1: "Bronze Tamer",
    2: "Silver Tamer",
    3: "Mystic Champion",
}


def banner():
    print(f"""{Colors.CYAN}
   _________________________________________
  /                                         \\
 |        T H E   M Y S T I C   A R E N A    |
  \\_________________________________________/
        where legends are forged in battle
{Colors.RESET}""")


def meet_the_bestiary():
    print(f"{Colors.YELLOW}Before you enter the arena, the keeper introduces the beasts you may bond with:{Colors.RESET}\n")
    dummy = Griffin("Echo")  # just here so battle_cry() has nothing to do with combat
    for cls in BESTIARY:
        preview = cls()
        print(f"  {Colors.MAGENTA}* {cls.__name__:<8}{Colors.RESET} -> \"{preview.battle_cry()}\"")
    print()


def choose_beast():
    print(f"{Colors.BOLD}Which creature calls to you?{Colors.RESET}")
    for i, cls in enumerate(BESTIARY, start=1):
        print(f"  {Colors.CYAN}{i}. {cls.__name__}{Colors.RESET}")
    while True:
        choice = input("> ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(BESTIARY):
            cls = BESTIARY[int(choice) - 1]
            break
        print(f"{Colors.RED}The keeper doesn't recognize that number. Try again.{Colors.RESET}")

    nickname = input(f"\nName your {cls.__name__} (leave blank to keep its true name): ").strip()
    beast = cls(nickname) if nickname else cls()
    print(f"\n{Colors.GREEN}{beast.name} the {cls.__name__} bonds with you. {beast.battle_cry()}{Colors.RESET}\n")
    return beast


def spawn_rival(round_number):
    """Each round summons a tougher wild rival."""
    cls = random.choice(BESTIARY)
    rival = cls(name=f"Wild {cls.__name__}")
    for _ in range(round_number - 1):
        rival.level_up()
    return rival


def show_status(player, rival):
    print()
    # Color player HP/MP
    player_hp_color = Colors.GREEN if player.health > player.max_health * 0.5 else Colors.YELLOW if player.health > player.max_health * 0.2 else Colors.RED
    player_mp_color = Colors.BLUE if player.mana > player.max_mana * 0.5 else Colors.CYAN if player.mana > player.max_mana * 0.2 else Colors.GRAY
    print(f"{player.name} | HP: {player_hp_color}{player.health}/{player.max_health}{Colors.RESET} | MP: {player_mp_color}{player.mana}/{player.max_mana}{Colors.RESET} | Lv.{player._level}")

    # Color rival HP/MP
    rival_hp_color = Colors.GREEN if rival.health > rival.max_health * 0.5 else Colors.YELLOW if rival.health > rival.max_health * 0.2 else Colors.RED
    rival_mp_color = Colors.BLUE if rival.mana > rival.max_mana * 0.5 else Colors.CYAN if rival.mana > rival.max_mana * 0.2 else Colors.GRAY
    print(f"{rival.name} | HP: {rival_hp_color}{rival.health}/{rival.max_health}{Colors.RESET} | MP: {rival_mp_color}{rival.mana}/{rival.max_mana}{Colors.RESET} | Lv.{rival._level}")


def player_turn(player, rival):
    print(f"\n{Colors.BOLD}Choose your action:{Colors.RESET}")
    print(f"{Colors.CYAN}1. Attack{Colors.RESET}   {Colors.MAGENTA}2. Special Ability{Colors.RESET}   {Colors.YELLOW}3. Check status{Colors.RESET}")
    while True:
        choice = input("> ").strip()
        if choice == "1":
            print(f"{Colors.WHITE}{player.attack(rival)}{Colors.RESET}")
            return
        elif choice == "2":
            print(f"{Colors.MAGENTA}{player.special_ability(rival)}{Colors.RESET}")
            return
        elif choice == "3":
            show_status(player, rival)
        else:
            print(f"{Colors.RED}Pick 1, 2, or 3.{Colors.RESET}")


def rival_turn(rival, player):
    if random.random() < 0.35:
        print(f"{Colors.RED}{rival.special_ability(player)}{Colors.RESET}")
    else:
        print(f"{Colors.RED}{rival.attack(player)}{Colors.RESET}")


def run_battle(player, rival, round_number):
    print(f"\n{Colors.BOLD}{'=' * 50}{Colors.RESET}")
    print(f"{Colors.YELLOW}ROUND {round_number}: {player.name} vs {rival.name}{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 50}{Colors.RESET}")
    print(f"{Colors.RED}{rival.battle_cry()}{Colors.RESET}")

    while player.is_alive() and rival.is_alive():
        show_status(player, rival)
        player_turn(player, rival)
        if not rival.is_alive():
            break
        rival_turn(rival, player)

    if player.is_alive():
        print(f"\n{Colors.GREEN}{rival.name} has been defeated! {player.name} stands victorious!{Colors.RESET}\n")
        return True
    else:
        print(f"\n{Colors.RED}{player.name} has fallen. The arena falls silent...{Colors.RESET}\n")
        return False


def between_rounds_event(player):
    """A little flavor and a small strategic choice between fights."""
    events = [
        ("A traveling healer offers to mend your wounds.", "heal"),
        ("A glowing spring restores your inner energy.", "mana"),
        ("The arena keeper offers no aid this time - press on.", "none"),
    ]
    text, kind = random.choice(events)
    print(f"\n{Colors.BLUE}--- {text} ---{Colors.RESET}")
    if kind == "heal":
        healed = player.heal(20)
        print(f"{Colors.GREEN}{player.name} recovers {healed} HP.{Colors.RESET}")
    elif kind == "mana":
        player.mana = player.mana + 15
        print(f"{Colors.CYAN}{player.name}'s mana is restored.{Colors.RESET}")
    else:
        print(f"{Colors.GRAY}Nothing changes, but you press forward anyway.{Colors.RESET}")
    player.level_up()
    print(f"{Colors.YELLOW}{player.name} grows stronger from the experience (now Lv.{player._level}).{Colors.RESET}\n")


def final_rank(wins):
    title = RANK_TITLES.get(wins, "Legend of the Arena")
    print(f"{Colors.BOLD}{'=' * 50}{Colors.RESET}")
    print(f"{Colors.MAGENTA}TOURNAMENT COMPLETE - Wins: {wins}/3{Colors.RESET}")
    print(f"{Colors.CYAN}Your title: {title}{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 50}{Colors.RESET}")


def main():
    banner()
    meet_the_bestiary()
    player = choose_beast()

    wins = 0
    for round_number in range(1, 4):
        rival = spawn_rival(round_number)
        won = run_battle(player, rival, round_number)
        if not won:
            break
        wins += 1
        if round_number < 3 and player.is_alive():
            between_rounds_event(player)

    final_rank(wins)


if __name__ == "__main__":
    main()