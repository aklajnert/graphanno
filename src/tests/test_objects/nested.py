"""Nested classes definition."""


class Leaf:
    """Leaf class definition."""
    value: str = ''


class TopLevel:
    """Top level class which references to Leaf."""
    leaf: Leaf = None
    name: str = ''
