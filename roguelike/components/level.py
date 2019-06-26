from dataclasses import dataclass


@dataclass
class Level:
    current_level: int = 1
    current_xp: int = 0
    level_up_base: int = 200
    level_up_factor: int = 150

    @property
    def experience_to_next_level(self):
        return self.level_up_base + self.current_level * self.level_up_factor

    def add_xp(self, xp):
        self.current_xp += xp

        if self.current_xp > self.experience_to_next_level:
            self.current_xp -= self.experience_to_next_level
            self.current_level += 1

            return True
        else:
            return False
