"""
test_roguelike.py

Tests for roguelike.
"""
from roguelike import __version__


def test_version():
    assert __version__ == "0.1.11"
