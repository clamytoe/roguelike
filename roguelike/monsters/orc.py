from roguelike.entity import Entity
from roguelike.components.fighter import Fighter
from roguelike.components.ai import BasicMonster
from roguelike.colors import Colors
from roguelike.render_functions import RenderOrder

class Orc(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char="o",
            color=Colors.desaturated_green,
            name="Orc",
            blocks=True,
            render_order=RenderOrder.ACTOR,
            fighter=Fighter(hp=20, defense=0, power=4, xp=35),
            ai=BasicMonster(),
        )
