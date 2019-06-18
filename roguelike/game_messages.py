import textwrap
from dataclasses import dataclass, field
from typing import List

import tcod
from tcod.color import Color


@dataclass
class Message:
    text: str
    color: Color = field(default_factory=Color)

    def __post_init__(self):
        if not self.color:
            self.color = tcod.white


@dataclass
class MessageLog:
    x: int
    width: int
    height: int
    messages: List[Message] = field(default_factory=list)

    def add_message(self, message: Message) -> None:
        """
        Split the message if necessary, among multiple lines
        :param message: Message object
        :return: None
        """
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # if the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == self.height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, message.color))
