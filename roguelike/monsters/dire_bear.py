from __future__ import annotations
from roguelike.entity import Entity
from roguelike.components.fighter import Fighter
from roguelike.components.ai import BasicMonster
from roguelike.colors import Colors
from roguelike.render_functions import RenderOrder

class DireBear(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char="B",
            color=Colors.dark_orange,
            name="Dire Bear",
            blocks=True,
            render_order=RenderOrder.ACTOR,
            fighter=Fighter(hp=30, defense=2, power=8, xp=120),
            ai=BasicMonster(),
        )
