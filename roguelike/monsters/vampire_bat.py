from __future__ import annotations
from roguelike.entity import Entity
from roguelike.components.fighter import Fighter
from roguelike.components.ai import BasicMonster
from roguelike.colors import Colors
from roguelike.render_functions import RenderOrder

class VampireBat(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char="b",
            color=Colors.dark_red,
            name="Vampire Bat",
            blocks=True,
            render_order=RenderOrder.ACTOR,
            fighter=Fighter(hp=8, defense=0, power=3, xp=30),
            ai=BasicMonster(),
        )
