"""Test no annotations."""
import pytest

from graphanno import graphanno


class NoAnnotations:
    """Class that doesn't have annotations."""
    field = 'str'
    other_field = True


class WithAnnotations:
    """This class have annotations, but will be excluded in test."""
    string: str
    boolean: bool


def test_no_annotations_raised():
    """Decorating the class without annotations will raise an exception."""
    with pytest.raises(graphanno.NoAnnotationsError) as excinfo:
        @graphanno.graph_annotations
        class _:
            __model__ = NoAnnotations

    assert excinfo.value.args[0] == "No included annotations for class _."


def test_with_annotations_raised():
    """The decorated class has annotations, but all fields are excluded which will raise exception."""
    with pytest.raises(graphanno.NoAnnotationsError) as excinfo:
        @graphanno.graph_annotations
        class _:
            __model__ = WithAnnotations
            __excluded_fields__ = ('string', 'boolean')

    assert excinfo.value.args[0] == "No included annotations for class _."
