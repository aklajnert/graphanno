"""Test pylint"""


class Example:
    """Example class"""

    def do_something(self):
        """Example method"""


class ExampleSuperclass(Example):
    """Superclass of the Example."""
    instance = None

    def do_something(self):
        """Example method override"""
        print('test')
        return super().do_something()

    def do_something_else(self, attr):
        """Another example method"""
        return getattr(self.instance, attr)
