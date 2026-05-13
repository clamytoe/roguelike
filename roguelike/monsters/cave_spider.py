from roguelike.entity import Entity
from roguelike.components.fighter import Fighter
from roguelike.components.ai import BasicMonster
from roguelike.colors import Colors
from roguelike.render_functions import RenderOrder

class CaveSpider(Entity):
    venom = {"chance": 0.25, "turns": 5, "damage": 2}
    venom_message = "bites you"

    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char="S",
            color=Colors.green,
            name="Snake",
            blocks=True,
            render_order=RenderOrder.ACTOR,
            fighter=Fighter(hp=14, defense=0, power=3, xp=25),
            ai=BasicMonster(),
        )
