from __future__ import annotations
from roguelike.entity import Entity
from roguelike.components.fighter import Fighter
from roguelike.components.ai import BasicMonster
from roguelike.colors import Colors
from roguelike.render_functions import RenderOrder

class Zombie(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char="Z",
            color=Colors.dark_green,
            name="Zombie",
            blocks=True,
            render_order=RenderOrder.ACTOR,
            fighter=Fighter(hp=20, defense=2, power=3, xp=50),
            ai=BasicMonster(),
        )
