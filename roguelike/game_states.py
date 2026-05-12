from enum import Enum, auto

class GameStates(Enum):
    # Core gameplay loop
    PLAYERS_TURN = auto()
    ENEMY_TURN = auto()
    PLAYER_DEAD = auto()

    # Modal UI states
    SHOW_INVENTORY = auto()
    DROP_INVENTORY = auto()
    TARGETING = auto()
    LEVEL_UP = auto()
    CHARACTER_SCREEN = auto()

    @property
    def is_player_turn(self):
        return self == GameStates.PLAYERS_TURN

    @property
    def is_enemy_turn(self):
        return self == GameStates.ENEMY_TURN

    @property
    def is_modal(self):
        return self in {
            GameStates.SHOW_INVENTORY,
            GameStates.DROP_INVENTORY,
            GameStates.TARGETING,
            GameStates.LEVEL_UP,
            GameStates.CHARACTER_SCREEN,
        }

    @property
    def blocks_input(self):
        return self.is_modal or self == GameStates.PLAYER_DEAD
