from roguelike.entity import Entity
from roguelike.components.fighter import Fighter
from roguelike.components.ai import BasicMonster
from roguelike.colors import Colors
from roguelike.render_functions import RenderOrder

class Goblin(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char="g",
            color=Colors.light_green,
            name="Goblin",
            blocks=True,
            render_order=RenderOrder.ACTOR,
            fighter=Fighter(hp=12, defense=0, power=3, xp=20),
            ai=BasicMonster(),
        )
