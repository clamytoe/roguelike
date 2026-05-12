from __future__ import annotations
from roguelike.entity import Entity
from roguelike.components.fighter import Fighter
from roguelike.components.ai import BasicMonster
from roguelike.colors import Colors
from roguelike.render_functions import RenderOrder

class Cultist(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char="c",
            color=Colors.violet,
            name="Cultist",
            blocks=True,
            render_order=RenderOrder.ACTOR,
            fighter=Fighter(hp=16, defense=1, power=6, xp=70),
            ai=BasicMonster(),
        )
