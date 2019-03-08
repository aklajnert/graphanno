"""Test advanced example."""

import graphene

import graphanno
from .test_objects.advanced import Advanced
from .utils import to_dict


@graphanno.graph_annotations
class AdvancedSchema(graphanno.ObjectType):
    """Wrapper for Advanced class."""

    __model__ = Advanced


class Query(graphene.ObjectType):
    """Test GraphQL query."""

    advanced = graphene.Field(AdvancedSchema)

    @staticmethod
    def resolve_advanced(*_):
        """Return the advanced object instance"""
        # pylint: disable=attribute-defined-outside-init
        data = Advanced()
        data.array = ["first", "second", "third"]
        return data


def test_advanced():
    """Test advanced class behavior."""
    # pylint: disable=no-member
    assert isinstance(AdvancedSchema.array, graphene.List)
    assert isinstance(AdvancedSchema.dynamic_value, graphene.Int)
    assert isinstance(AdvancedSchema.optional, graphene.String)
    assert issubclass(AdvancedSchema, graphene.ObjectType)
    assert not hasattr(AdvancedSchema, "_private")
    assert not hasattr(AdvancedSchema, "not_annotated_property")


def test_query():
    """Test real query with generated object."""
    schema = graphene.Schema(query=Query)
    response = schema.execute("{ advanced {array, dynamicValue, optional} }")
    assert to_dict(response.data) == {
        "advanced": {
            "array": ["first", "second", "third"],
            "dynamicValue": 5,
            "optional": None,
        }
    }
