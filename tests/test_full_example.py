"""Test full example containing all features."""
import graphene

from graphanno import graph_annotations
from .test_objects.full_example import Example


@graph_annotations
class ExampleSchema:
    """Graphene object that bases on Example class."""
    __model__ = Example
    __excluded_fields__ = ('redundant',)


def test_example_schema():
    """Check the object fields."""
    # pylint: disable=no-member
    assert issubclass(ExampleSchema, graphene.ObjectType)
    assert not hasattr(ExampleSchema, 'redundant')
    assert isinstance(ExampleSchema.name, graphene.String)
    assert isinstance(ExampleSchema.amount_round, graphene.Int)
    assert isinstance(ExampleSchema.amount, graphene.Float)
    assert isinstance(ExampleSchema.useful, graphene.Boolean)
    assert isinstance(ExampleSchema.created, graphene.DateTime)
    assert isinstance(ExampleSchema.expiration, graphene.Date)
    assert isinstance(ExampleSchema.refresh_at, graphene.Time)
    assert isinstance(ExampleSchema.owner, graphene.Field)
    assert str(ExampleSchema.owner.type) == 'Owner'
    assert isinstance(ExampleSchema.owner.type.name, graphene.String)
    assert isinstance(ExampleSchema.tags, graphene.List)
    assert str(ExampleSchema.tags.of_type) == 'Tag'
