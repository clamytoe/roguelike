from __future__ import annotations
from roguelike.entity import Entity
from roguelike.components.fighter import Fighter
from roguelike.components.ai import BasicMonster
from roguelike.colors import Colors
from roguelike.render_functions import RenderOrder

class GiantRat(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char="r",
            color=Colors.light_grey,
            name="Giant Rat",
            blocks=True,
            render_order=RenderOrder.ACTOR,
            fighter=Fighter(hp=6, defense=0, power=2, xp=20),
            ai=BasicMonster(),
        )
