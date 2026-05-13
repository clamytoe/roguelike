from roguelike.colors import Colors
from roguelike.game_messages import Message
from roguelike.item_functions import cast_fireball

from .base_item import BaseItem


class FireballScroll(BaseItem):
    char = "#"
    color = Colors.red
    name = "Fireball Scroll"
    use_function = cast_fireball
    targeting = True
    targeting_message = Message(
        "Left-click a target tile for the fireball, or right-click to cancel",
        Colors.light_cyan,
    )
    function_kwargs = {"damage": 25, "radius": 3}
