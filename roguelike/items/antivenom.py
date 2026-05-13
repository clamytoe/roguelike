from roguelike.colors import Colors
from roguelike.game_messages import Message
from roguelike.item_functions import cure_poison
from .base_item import BaseItem

class Antivenom(BaseItem):
    char = "!"
    color = Colors.green
    name = "Antivenom"

    use_function = cure_poison
    function_kwargs = {}
