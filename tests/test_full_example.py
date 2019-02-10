# pylint: disable=arguments-differ
"""Test full example containing all features."""
import graphene

from graphanno import graph_annotations
from .test_objects.full_example import Example
from .utils import to_dict


@graph_annotations
class ExampleSchema(graphene.ObjectType):
    """Graphene object that bases on Example class."""
    __model__ = Example
    __excluded_fields__ = ('redundant',)

    instance = Example.create_instance()

    @classmethod
    def __init_subclass_with_meta__(cls, *args, **kwargs):
        return super().__init_subclass_with_meta__(
            *args, default_resolver=cls._default_fields_resolver, **kwargs)

    @classmethod
    def _default_fields_resolver(cls, attr_name, *_):
        return getattr(cls.instance, attr_name)


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


def test_example_query():
    """Check behavior of the annotated class."""
    schema = graphene.Schema(query=ExampleSchema)
    response = schema.execute('{ name }')
    assert to_dict(response.data) == {'name': 'Full feature'}
