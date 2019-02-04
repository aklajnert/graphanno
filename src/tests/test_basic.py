"""Test basic example."""
from collections import OrderedDict

import graphene

from .test_objects.basic import Basic
from ..graphanno import graph_annotations


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


class Query(graphene.ObjectType):
    """Test GraphQL query."""
    basic = graphene.Field(ExtendedBasicSchema)

    @staticmethod
    def resolve_basic(*_):
        """Return the basic object instance"""
        # pylint: disable=attribute-defined-outside-init
        data = ExtendedBasicSchema()
        data.extra = False
        data.boolean = 5
        data.number = 10
        data.string = 'some string'
        return data


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


def test_query():
    """Test graphene query with the generated object."""
    schema = graphene.Schema(query=Query)
    response = schema.execute('{basic {extra, boolean, number, string} }')
    assert response.data == OrderedDict([
        ('basic', OrderedDict([
            ('extra', False),
            ('boolean', 5),
            ('number', 10),
            ('string', 'some string')]))])
