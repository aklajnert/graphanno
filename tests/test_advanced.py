"""Test advanced example."""

import graphene

from graphanno import graph_annotations
from .test_objects.advanced import Advanced
from .utils import to_dict


@graph_annotations
class AdvancedSchema:
    """Wrapper for Advanced class."""
    __model__ = Advanced


class Query(graphene.ObjectType):
    """Test GraphQL query."""
    advanced = graphene.Field(AdvancedSchema)

    @staticmethod
    def resolve_advanced(*_):
        """Return the advanced object instance"""
        # pylint: disable=attribute-defined-outside-init
        data = AdvancedSchema()
        data.array = ['first', 'second', 'third']
        return data


def test_advanced():
    """Test advanced class behavior."""
    # pylint: disable=no-member
    assert isinstance(AdvancedSchema.array, graphene.List)
    assert issubclass(AdvancedSchema, graphene.ObjectType)


def test_query():
    """Test real query with generated object."""
    schema = graphene.Schema(query=Query)
    response = schema.execute('{ advanced {array} }')
    assert to_dict(response.data) == {'advanced': {'array': ['first', 'second', 'third']}}
