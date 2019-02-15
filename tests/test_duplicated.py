"""Test duplicate behavior."""

import graphene

import graphanno
from .test_objects import duplicated
from .utils import to_dict


@graphanno.graph_annotations
class Duplicated:
    """Wrapper for the Duplicate class. The name is purposely the same as the name of the model,
    this will cause the name clash"""
    __model__ = duplicated.Duplicated


@graphanno.graph_annotations
class DuplicateUser:
    """Wrapper for DuplicateUser."""
    __model__ = duplicated.DuplicateUser


class Query(graphene.ObjectType):
    """Test GraphQL query."""
    user = graphene.Field(DuplicateUser)
    duplicate = graphene.Field(Duplicated)

    def resolve_user(self, *_):
        """Return the DuplicateUser object instance"""
        # pylint: disable=attribute-defined-outside-init
        data = duplicated.DuplicateUser()
        data.duplicate = self.resolve_duplicate()
        data.name = 'duplicated_parent'
        return data

    @staticmethod
    def resolve_duplicate(*_):
        """Return the Duplicated object instance"""
        # pylint: disable=attribute-defined-outside-init
        duplicate = duplicated.Duplicated()
        duplicate.name = 'duplicated_child'


def test_schema():
    """Test DuplicatedUser content."""
    # pylint: disable=no-member
    assert isinstance(DuplicateUser.name, graphene.String)
    assert isinstance(DuplicateUser.duplicate, graphene.Field)
    assert issubclass(DuplicateUser, graphene.ObjectType)


def test_query():
    """Test graphene query with the generated object."""
    schema = graphene.Schema(query=Query)
    response = schema.execute('{data {name, duplicate {name} }}')
    assert to_dict(response.data) == {
        'data': {
            'name': 'duplicated_parent',
            'duplicate': {'name': 'duplicated_child'}
        }
    }
