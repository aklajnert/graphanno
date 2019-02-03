"""Test example with excluding."""

import graphene

from .test_objects.basic import Basic
from ..graphanno import graph_annotations


@graph_annotations
class ExcludingSchema:
    """Wrapper for the Basic class with excluding few keys."""
    __model__ = Basic
    __excluded_fields__ = ('number', 'boolean')


def test_excluded():
    """Test case with excluded fields."""
    # pylint: disable=no-member
    assert isinstance(ExcludingSchema.string, graphene.String)
    assert not hasattr(ExcludingSchema, 'boolean')
    assert not hasattr(ExcludingSchema, 'number')
    assert issubclass(ExcludingSchema, graphene.ObjectType)
