from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Union


@dataclass(init=False)
class Item:
    use_function: Union[Callable, None]
    targeting: bool
    targeting_message: Union[str, None]
    function_kwargs: Mapping[Any, Any]

    def __init__(
        self, use_function=None, targeting=False, targeting_message=None, **kwargs
    ):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs
