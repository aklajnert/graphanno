"""Test basic example."""
import graphene

from src.graphanno import graph_annotations
from .test_objects.basic import Basic


@graph_annotations
class BasicSchema:
    """Wrapper for the Basic class."""
    __model__ = Basic


def test_basic():
    """Test basic case."""
    # pylint: disable=no-member
    assert isinstance(BasicSchema.number, graphene.Int)
    assert isinstance(BasicSchema.string, graphene.String)
    assert isinstance(BasicSchema.boolean, graphene.Boolean)
    assert issubclass(BasicSchema, graphene.ObjectType)
