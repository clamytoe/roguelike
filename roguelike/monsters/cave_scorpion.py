from __future__ import annotations
from roguelike.entity import Entity
from roguelike.components.fighter import Fighter
from roguelike.components.ai import BasicMonster
from roguelike.colors import Colors
from roguelike.render_functions import RenderOrder

class CaveScorpion(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char="s",
            color=Colors.orange,
            name="Cave Scorpion",
            blocks=True,
            render_order=RenderOrder.ACTOR,
            fighter=Fighter(hp=12, defense=1, power=5, xp=45),
            ai=BasicMonster(),
        )
