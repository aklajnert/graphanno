"""Advanced class definition."""
from typing import List


class Advanced:
    """Class with advanced data types."""
    array: List[str]
    _private: bool

    @property
    def dynamic_value(self) -> int:
        """Dynamic property"""
        return 5
