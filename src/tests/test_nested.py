"""Test example with nesting."""
import graphene

from .test_objects.nested import TopLevel
from ..graphanno import graph_annotations


@graph_annotations
class NestedSchema:
    """Class that uses TopLevel class as nested model."""
    __model__ = TopLevel


def test_nested():
    """Validate result of the nested class resolving."""
    # pylint: disable=no-member
    assert issubclass(NestedSchema, graphene.ObjectType)
    assert isinstance(NestedSchema.name, graphene.String)
    assert isinstance(NestedSchema.leaf, graphene.Field)
    assert isinstance(NestedSchema.leaf.type.value, graphene.String)
