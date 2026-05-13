from roguelike.colors import Colors
from roguelike.components.item import Item
from roguelike.entity import Entity
from roguelike.render_functions import RenderOrder


class BaseItem(Entity):
    char = "!"
    color = Colors.white
    name = "Item"
    use_function = None
    targeting = False
    targeting_message = None
    function_kwargs = {}

    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y,
            char=self.char,
            color=self.color,
            name=self.name,
            render_order=RenderOrder.ITEM,
            item=Item(
                use_function=self.__class__.use_function,
                targeting=self.targeting,
                targeting_message=self.targeting_message,
                **self.__class__.function_kwargs
            ),
        )
