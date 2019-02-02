"""Test advanced example."""
import graphene

from .test_objects.advanced import Advanced
from ..graphanno import graph_annotations


@graph_annotations
class AdvancedSchema:
    """Wrapper for Advanced class."""
    __model__ = Advanced


def test_advanced():
    """Test advanced class behavior."""
    # pylint: disable=no-member
    assert isinstance(AdvancedSchema.array, graphene.List)
    assert issubclass(AdvancedSchema, graphene.ObjectType)
