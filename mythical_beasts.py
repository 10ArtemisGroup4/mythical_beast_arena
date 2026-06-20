from abc import ABC, abstractmethod
import random


class MythicalBeast(ABC):
    """The Abstract Base Class showcasing Abstraction, Encapsulation, and Elemental rules."""

    def __init__(self, name: str, health: int, attack_power: int, speed: int, beast_type: str, element: str):
        self.name = name
        self.beast_type = beast_type
        self.element = element

        # Encapsulation: Protected combat attributes
        self._max_health = health
        self._health = health
        self._attack_power = attack_power
        self._speed = speed
        self._ultimate_gauge = 0

    @property
    def health(self) -> int:
        return max(0, self._health)

    @property
    def max_health(self) -> int:
        return self._max_health

    @property
    def attack_power(self) -> int:
        return self._attack_power

    @property
    def speed(self) -> int:
        return self._speed

    @property
    def ultimate_gauge(self) -> int:
        return min(100, self._ultimate_gauge)

    def recover_health(self, amount: int):
        """Allows safely modifying health states between ladder matches."""
        self._health = min(self._max_health, self._health + amount)

    def scale_difficulty(self, multiplier: float):
        """Scales up enemy attributes for the endless survival mode progression."""
        self._max_health = int(self._max_health * multiplier)
        self._health = self._max_health
        self._attack_power = int(self._attack_power * multiplier)

    def calculate_elemental_multiplier(self, opponent: 'MythicalBeast') -> float:
        """Calculates strict rock-paper-scissors type balancing logic."""
        rules = {
            "Fire": "Water",  # Fire is weak against Water
            "Water": "Air",  # Water is weak against Air
            "Air": "Fire"  # Air is weak against Fire
        }
        if rules.get(self.element) == opponent.element:
            return 0.75  # Disadvantage
        if rules.get(opponent.element) == self.element:
            return 1.5  # Advantage
        return 1.0  # Neutral

    def take_damage(self, amount: int) -> str:
        """Deducts life points and charges the passive ultimate gauge asset."""
        actual_damage = max(1, amount)
        self._health -= actual_damage
        if self._health < 0:
            self._health = 0

        # Passive Ultimate Gauge: Charges based on damage sustained
        charge_gained = int(actual_damage * 0.8)
        self._ultimate_gauge = min(100, self._ultimate_gauge + charge_gained)

        return f"{self.name} takes {actual_damage} damage! (Ultimate Gauge +{charge_gained}%)"

    def basic_attack(self, opponent: 'MythicalBeast') -> str:
        """Shared attacking mechanics augmented by custom type values."""
        base = random.randint(self._attack_power - 3, self._attack_power + 3)
        mult = self.calculate_elemental_multiplier(opponent)
        damage = int(base * mult)

        log = f"[ATTACK] {self.name} ({self.element}) strikes {opponent.name} ({opponent.element}).\n"
        if mult > 1.0:
            log += "[EFFECT] Structural advantage! Exploiting weakness.\n"
        elif mult < 1.0:
            log += "[EFFECT] Elemental resistance! Attack was suppressed.\n"

        log += opponent.take_damage(damage)
        return log

    @abstractmethod
    def execute_special_ability(self, opponent: 'MythicalBeast') -> str:
        """Abstraction Pillar: Forced subclass signature implementation."""
        pass

    @abstractmethod
    def execute_ultimate_ability(self, opponent: 'MythicalBeast') -> str:
        """Abstraction Pillar: Charged ultimate logic requirements."""
        pass


# Inheritance Pillar: Distinct specialized child classes
class Dragon(MythicalBeast):
    """Fire element asset targeting offensive output metrics."""

    def __init__(self, name: str):
        super().__init__(name, health=140, attack_power=22, speed=12, beast_type="Dragon", element="Fire")

    def execute_special_ability(self, opponent: 'MythicalBeast') -> str:
        mult = self.calculate_elemental_multiplier(opponent)
        damage = int((self._attack_power * 1.7) * mult)
        log = f"[SPECIAL] {self.name} unleashes a devastating magma burst!\n"
        log += opponent.take_damage(damage)
        return log

    def execute_ultimate_ability(self, opponent: 'MythicalBeast') -> str:
        self._ultimate_gauge = 0
        mult = self.calculate_elemental_multiplier(opponent)
        damage = int((self._attack_power * 2.8) * mult)
        log = f"[ULTIMATE] {self.name} activates CATACLYSMIC SUPERNOVA, melting the landscape!\n"
        log += opponent.take_damage(damage)
        return log


class Phoenix(MythicalBeast):
    """Air element asset built around restoration speed loops."""

    def __init__(self, name: str):
        super().__init__(name, health=100, attack_power=15, speed=25, beast_type="Phoenix", element="Air")

    def execute_special_ability(self, opponent: 'MythicalBeast') -> str:
        heal_amount = 30
        self.recover_health(heal_amount)
        mult = self.calculate_elemental_multiplier(opponent)
        damage = int((self._attack_power * 1.1) * mult)

        log = f"[SPECIAL] {self.name} flashes with blinding solar heat!\n"
        log += f"[HEAL] {self.name} recovers {heal_amount} health points.\n"
        log += opponent.take_damage(damage)
        return log

    def execute_ultimate_ability(self, opponent: 'MythicalBeast') -> str:
        self._ultimate_gauge = 0
        heal_amount = self._max_health - self._health
        self.recover_health(heal_amount)
        mult = self.calculate_elemental_multiplier(opponent)
        damage = int((self._attack_power * 1.5) * mult)

        log = f"[ULTIMATE] {self.name} triggers NIRVANA REBIRTH, fully restoring structural health and creating a shockwave!\n"
        log += f"[HEAL] {self.name} completely refreshed health reserves.\n"
        log += opponent.take_damage(damage)
        return log


class Kraken(MythicalBeast):
    """Water element asset scaled for high vitality profiles."""

    def __init__(self, name: str):
        super().__init__(name, health=190, attack_power=14, speed=8, beast_type="Kraken", element="Water")

    def execute_special_ability(self, opponent: 'MythicalBeast') -> str:
        mult = self.calculate_elemental_multiplier(opponent)
        damage = int((self._attack_power + 8) * mult)
        opponent._attack_power = max(5, opponent._attack_power - 4)

        log = f"[SPECIAL] {self.name} drags the opponent into an icy whirlpool squeeze!\n"
        log += f"[DEBUFF] {opponent.name}'s attack power fell by 4 points.\n"
        log += opponent.take_damage(damage)
        return log

    def execute_ultimate_ability(self, opponent: 'MythicalBeast') -> str:
        self._ultimate_gauge = 0
        mult = self.calculate_elemental_multiplier(opponent)
        damage = int((self._attack_power * 2.2) * mult)
        opponent._speed = max(2, opponent._speed - 10)

        log = f"[ULTIMATE] {self.name} invokes TIDAL DELUGE, paralyzing the target in heavy currents!\n"
        log += f"[DEBUFF] {opponent.name}'s mechanical speed was crippled.\n"
        log += opponent.take_damage(damage)
        return log
