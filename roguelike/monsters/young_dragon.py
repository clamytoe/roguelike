from __future__ import annotations
from roguelike.entity import Entity
from roguelike.components.fighter import Fighter
from roguelike.components.ai import BasicMonster
from roguelike.colors import Colors
from roguelike.render_functions import RenderOrder

class YoungDragon(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char="D",
            color=Colors.red,
            name="Young Dragon",
            blocks=True,
            render_order=RenderOrder.ACTOR,
            fighter=Fighter(hp=50, defense=4, power=10, xp=200),
            ai=BasicMonster(),
        )
