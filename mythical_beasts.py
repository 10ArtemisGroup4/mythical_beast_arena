
from abc import ABC, abstractmethod
import random


class MythicalBeast(ABC):
    """Abstract base class - the magical contract every beast must obey."""

    def __init__(self, name, max_health, max_mana, base_power):
        self._name = name
        self.__max_health = max_health
        self.__health = max_health          # private -> encapsulated
        self.__max_mana = max_mana
        self.__mana = max_mana              # private -> encapsulated
        self._base_power = base_power
        self._level = 1

    # ---------------- Encapsulation: guarded access only ----------------
    @property
    def name(self):
        return self._name

    @property
    def max_health(self):
        return self.__max_health

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        # No matter who calls this, health can never leave [0, max_health]
        self.__health = max(0, min(value, self.__max_health))

    @property
    def mana(self):
        return self.__mana

    @mana.setter
    def mana(self, value):
        self.__mana = max(0, min(value, self.__max_mana))

    def is_alive(self):
        return self.__health > 0

    def take_damage(self, amount):
        self.health = self.health - amount   # routed through the setter
        return amount

    def heal(self, amount):
        before = self.health
        self.health = self.health + amount
        return self.health - before

    def spend_mana(self, amount):
        if self.__mana >= amount:
            self.mana = self.mana - amount
            return True
        return False

    def level_up(self):
        self._level += 1
        self._base_power += 2
        self.heal(10)

    # ------------------------- Abstraction -------------------------
    @abstractmethod
    def attack(self, target):
        """Every beast must define its own basic attack."""
        raise NotImplementedError

    @abstractmethod
    def special_ability(self, target=None):
        """Every beast must define its own unique special move."""
        raise NotImplementedError

    @abstractmethod
    def battle_cry(self):
        """Every beast must define its own roar/cry."""
        raise NotImplementedError

    # ------------------------- Shared utility -------------------------
    def status_bar(self, width=20):
        ratio = self.health / self.max_health if self.max_health else 0
        filled = int(width * ratio)
        bar = "#" * filled + "." * (width - filled)
        return f"{self._name:<10} [{bar}] {self.health:>3}/{self.max_health} HP | {self.mana:>3} MP"

    def __str__(self):
        return f"{self._name} (Lv.{self._level})"


class Dragon(MythicalBeast):
    """A fire-breathing brute that builds up rage with every claw swipe."""

    def __init__(self, name="Drakon"):
        super().__init__(name, max_health=120, max_mana=40, base_power=18)
        self.__fire_charge = 0  # private to Dragon only

    def attack(self, target):
        dmg = self._base_power + random.randint(-3, 5)
        self.__fire_charge += 1
        target.take_damage(dmg)
        return f"[Dragon] {self.name} claws {target.name} for {dmg} damage!"

    def special_ability(self, target=None):
        if target and self.spend_mana(15):
            dmg = self._base_power * 2 + self.__fire_charge
            target.take_damage(dmg)
            self.__fire_charge = 0
            return f"[Dragon] {self.name} unleashes an INFERNO BREATH on {target.name} for {dmg} damage!"
        return f"{self.name} doesn't have enough mana to breathe fire!"

    def battle_cry(self):
        return f"{self.name} roars, scorching the sky with flame!"


class Phoenix(MythicalBeast):
    """A graceful flier that can cheat death exactly once per battle."""

    def __init__(self, name="Ashera"):
        super().__init__(name, max_health=90, max_mana=60, base_power=14)
        self.__has_revived = False

    def attack(self, target):
        dmg = self._base_power + random.randint(0, 4)
        target.take_damage(dmg)
        return f"[Phoenix] {self.name} dives and slashes {target.name} for {dmg} damage!"

    def special_ability(self, target=None):
        if self.spend_mana(20):
            healed = self.heal(25)
            return f"[Phoenix] {self.name} bathes in healing flame, recovering {healed} HP!"
        return f"{self.name} is out of mana to self-heal!"

    def take_damage(self, amount):
        # Overridden on purpose: same call signature, very different behavior
        super().take_damage(amount)
        if not self.is_alive() and not self.__has_revived:
            self.__has_revived = True
            self.health = self.max_health // 2
            print(f"  *** {self.name} bursts into flame and is REBORN FROM ASHES with {self.health} HP! ***")
        return amount

    def battle_cry(self):
        return f"{self.name} cries out, eternal and undying!"


class Kraken(MythicalBeast):
    """A heavy-hitting sea titan that can drain an opponent's mana."""

    def __init__(self, name="Nautilon"):
        super().__init__(name, max_health=150, max_mana=30, base_power=20)

    def attack(self, target):
        dmg = self._base_power + random.randint(-5, 2)
        target.take_damage(dmg)
        return f"[Kraken] {self.name} smashes {target.name} with a tentacle for {dmg} damage!"

    def special_ability(self, target=None):
        if target and self.spend_mana(18):
            dmg = int(self._base_power * 1.5)
            target.take_damage(dmg)
            target.mana = target.mana - 10   # still goes through target's own setter
            return (f"[Kraken] {self.name} summons a MAELSTROM, dealing {dmg} damage "
                    f"and draining {target.name}'s mana!")
        return f"{self.name} doesn't have enough mana for a maelstrom!"

    def battle_cry(self):
        return f"{self.name} bellows from the deep, churning the seas!"


class Griffin(MythicalBeast):
    """A swift aerial striker with a chance to land critical hits."""

    def __init__(self, name="Skytalon"):
        super().__init__(name, max_health=100, max_mana=45, base_power=16)

    def attack(self, target):
        crit = random.random() < 0.25
        dmg = self._base_power * (2 if crit else 1) + random.randint(-2, 3)
        target.take_damage(dmg)
        tag = " (CRITICAL HIT!)" if crit else ""
        return f"[Griffin] {self.name} dive-bombs {target.name} for {dmg} damage!{tag}"

    def special_ability(self, target=None):
        if self.spend_mana(12):
            self._base_power += 3
            healed = self.heal(8)
            return f"[Griffin] {self.name} rides a mountain gale - power up, and heals {healed} HP!"
        return f"{self.name} lacks the mana to summon wind!"

    def battle_cry(self):
        return f"{self.name} shrieks a piercing battle cry across the mountains!"