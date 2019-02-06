"""Test example with nesting."""

import graphene

from graphanno import graph_annotations
from .test_objects.nested import TopLevel, Leaf, SubLeaf
from .utils import to_dict


@graph_annotations
class NestedSchema:
    """Class that uses TopLevel class as nested model."""
    __model__ = TopLevel


class NestedQuery(graphene.ObjectType):
    """Query using nested class."""
    top_level = graphene.Field(NestedSchema)

    @staticmethod
    def resolve_top_level(*_):
        """Return the top level object instance"""
        # pylint: disable=attribute-defined-outside-init
        data = TopLevel()
        subleaf1 = SubLeaf()
        subleaf1.value = 'subleaf1'
        subleaf2 = SubLeaf()
        subleaf2.value = 'subleaf2'
        leaf = Leaf()
        leaf.leaflets = [subleaf1, subleaf2]
        leaf.value = 'some leaf value'
        data.leaf = leaf
        data.name = 'top level name'
        return data


def test_nested():
    """Validate result of the nested class resolving."""
    # pylint: disable=no-member
    assert issubclass(NestedSchema, graphene.ObjectType)
    assert isinstance(NestedSchema.name, graphene.String)
    assert isinstance(NestedSchema.leaf, graphene.Field)
    assert str(NestedSchema.leaf.type) == 'Leaf'
    assert isinstance(NestedSchema.leaf.type.value, graphene.String)
    assert isinstance(NestedSchema.leaf.type.leaflets, graphene.List)


def test_nested_query():
    """Test the nested class behavior as a query."""
    schema = graphene.Schema(query=NestedQuery)
    response = schema.execute('{topLevel {name, leaf {value , leaflets {value} } } }')
    assert to_dict(response.data) == {
        'topLevel':
            {
                'name': 'top level name',
                'leaf':
                    {
                        'value': 'some leaf value',
                        'leaflets': [
                            {'value': 'subleaf1'},
                            {'value': 'subleaf2'}]
                    }
            }
    }
