from __future__ import annotations

import textwrap
from dataclasses import dataclass, field
from typing import List

from roguelike.colors import Color, Colors


# ---------------------------------------------------------------------------
# Message
# ---------------------------------------------------------------------------

@dataclass
class Message:
    """
    Represents a single line of text in the message log.
    """
    text: str
    color: Color

    def __post_init__(self):
        # Color is required; fallback removed to avoid masking bugs.
        if self.color is None:
            self.color = Colors.white

    def __repr__(self) -> str:
        return f"Message(text={self.text!r}, color={self.color})"


# ---------------------------------------------------------------------------
# Message Log
# ---------------------------------------------------------------------------

@dataclass
class MessageLog:
    """
    Stores and displays a scrolling list of messages.
    Handles line wrapping and buffer size limits.
    """
    x: int
    width: int
    height: int
    messages: List[Message] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Add a message (with wrapping)
    # ------------------------------------------------------------------
    def add_message(self, message: Message) -> None:
        """
        Add a message to the log, splitting it into multiple lines if needed.
        """            
        wrapped_lines = textwrap.wrap(message.text, self.width)

        for line in wrapped_lines:
            if len(self.messages) == self.height:
                self.messages.pop(0)

            self.messages.append(Message(line, message.color))

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------
    def add(self, text: str, color: Color = Colors.white) -> None:
        """
        Convenience wrapper to add a message without manually creating Message().
        """
        self.add_message(Message(text, color))

    def clear(self) -> None:
        """Remove all messages from the log."""
        self.messages.clear()

    def __repr__(self) -> str:
        return f"MessageLog({len(self.messages)} messages)"
