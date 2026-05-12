from __future__ import annotations
from roguelike.entity import Entity
from roguelike.components.fighter import Fighter
from roguelike.components.ai import BasicMonster
from roguelike.colors import Colors
from roguelike.render_functions import RenderOrder

class PitViper(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char="v",
            color=Colors.green,
            name="Pit Viper",
            blocks=True,
            render_order=RenderOrder.ACTOR,
            fighter=Fighter(hp=10, defense=1, power=4, xp=40),
            ai=BasicMonster(),
        )
