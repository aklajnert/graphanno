"""Test basic example."""
import graphene

from src.graphanno import graph_annotations
from .test_objects.basic import Basic


@graph_annotations
class BasicSchema:
    """Wrapper for the Basic class."""
    __model__ = Basic


@graph_annotations
class ExtendedBasicSchema:
    """Basic class with few additional fields."""
    __model__ = Basic

    extra: bool
    boolean: int  # override declaration from basic


def test_basic():
    """Test basic case."""
    # pylint: disable=no-member
    assert isinstance(BasicSchema.number, graphene.Int)
    assert isinstance(BasicSchema.string, graphene.String)
    assert isinstance(BasicSchema.boolean, graphene.Boolean)
    assert issubclass(BasicSchema, graphene.ObjectType)


def test_extended_basic():
    """Test extended basic case."""
    # pylint: disable=no-member
    assert isinstance(ExtendedBasicSchema.number, graphene.Int)
    assert isinstance(ExtendedBasicSchema.string, graphene.String)
    assert isinstance(ExtendedBasicSchema.boolean, graphene.Int)
    assert isinstance(ExtendedBasicSchema.extra, graphene.Boolean)
    assert issubclass(ExtendedBasicSchema, graphene.ObjectType)
