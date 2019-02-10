"""Test pylint"""


class Example:
    """Example class"""

    @classmethod
    def do_something(cls, data):
        """Example method"""
        print(data)


class ExampleSuperclass(Example):
    """Superclass of the Example."""
    instance = None

    @classmethod
    def do_something(cls, _):
        """Example method override"""
        return super().do_something('test')

    @classmethod
    def do_something_else(cls, attr):
        """Another example method"""
        return getattr(cls.instance, attr)
