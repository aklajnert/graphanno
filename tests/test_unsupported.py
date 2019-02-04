"""Test unsupported types."""
import graphene
import pytest

from graphanno import graphanno


class Unsupported:
    """Class that uses unsupported types."""
    array: list = []
    string: str = 'test'


def test_exception_raised():
    """Decorating the class refering to Unsupported will raise an exception."""
    with pytest.raises(graphanno.UnsupportedAnnotationError) as excinfo:
        @graphanno.graph_annotations
        class _:
            __model__ = Unsupported

    assert excinfo.value.args[0] == "The type annotation: <class 'list'> is not supported."


def test_exception_not_raised():
    """Decorating the class referring to Unsupported will not raise an exception because of
    the __ignore_unsupported__ flag.
    """

    @graphanno.graph_annotations
    class UnsupportedSchema:
        """Wrapping Unsupported class."""
        __model__ = Unsupported
        __ignore_unsupported__ = True

    # pylint: disable=no-member
    assert issubclass(UnsupportedSchema, graphene.ObjectType)
    assert not hasattr(UnsupportedSchema, 'array')
    assert isinstance(UnsupportedSchema.string, graphene.String)
