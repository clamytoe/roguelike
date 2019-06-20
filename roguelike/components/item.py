from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Union


@dataclass(init=False)
class Item:
    use_function: Union[Callable, None]
    function_kwargs: Mapping[Any, Any]

    def __init__(self, use_function=None, **kwargs):
        self.use_function = use_function
        self.function_kwargs = kwargs
