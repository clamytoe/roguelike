from roguelike.colors import Colors
from roguelike.game_messages import Message
from roguelike.item_functions import cast_confuse

from .base_item import BaseItem


class ConfusionScroll(BaseItem):
    char = "#"
    color = Colors.light_pink
    name = "Confusion Scroll"
    use_function = cast_confuse
    targeting = True
    targeting_message = Message(
        "Left-click an enemy to confuse it, or right-click to cancel.",
        Colors.light_cyan,
    )
