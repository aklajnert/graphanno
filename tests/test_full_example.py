# pylint: disable=arguments-differ,multiple-statements
"""Test full example containing all features."""
import graphene

from graphanno import graph_annotations
from .test_objects.full_example import Example
from .utils import to_dict


@graph_annotations
class ExampleSchema:
    """Graphene object that bases on Example class."""

    __model__ = Example
    __excluded_fields__ = ("redundant",)

    instance = Example.create_instance()

    @classmethod
    def __init_subclass_with_meta__(cls, *args, **kwargs):
        return super().__init_subclass_with_meta__(  # pylint: disable=no-member
            *args, default_resolver=cls._default_fields_resolver, **kwargs
        )

    @classmethod
    def _default_fields_resolver(cls, attr_name, *_):
        return getattr(cls.instance, attr_name)


def test_example_schema():
    """Check the object fields."""
    # pylint: disable=no-member
    assert issubclass(ExampleSchema, graphene.ObjectType)
    assert not hasattr(ExampleSchema, "redundant")
    assert isinstance(ExampleSchema.name, graphene.String)
    assert isinstance(ExampleSchema.amount_round, graphene.Int)
    assert isinstance(ExampleSchema.amount, graphene.Float)
    assert isinstance(ExampleSchema.useful, graphene.Boolean)
    assert isinstance(ExampleSchema.created, graphene.DateTime)
    assert isinstance(ExampleSchema.expiration, graphene.Date)
    assert isinstance(ExampleSchema.refresh_at, graphene.Time)
    assert isinstance(ExampleSchema.owner, graphene.Field)
    assert str(ExampleSchema.owner.type) == "Owner"
    assert isinstance(ExampleSchema.owner.type.name, graphene.String)
    assert isinstance(ExampleSchema.tags, graphene.List)
    assert str(ExampleSchema.tags.of_type) == "Tag"
    assert isinstance(ExampleSchema.double_amount, graphene.Float)


def test_example_query():
    """Check behavior of the annotated class."""
    schema = graphene.Schema(query=ExampleSchema)
    response = schema.execute(
        "{ name, amount, doubleAmount, amountRound, useful, created, expiration,"
        " refreshAt, owner { name }, tags { name } }"
    )
    assert to_dict(response.data) == {
        "name": "Full feature",
        "amount": 5.3,
        "doubleAmount": 10.6,
        "amountRound": 5,
        "useful": True,
        "created": "2019-02-06T15:00:00",
        "expiration": "2050-12-31",
        "refreshAt": "12:30:00",
        "owner": {"name": "me"},
        "tags": [{"name": "graphene"}, {"name": "type annotations"}],
    }
