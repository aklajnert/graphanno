"""Test duplicate behavior."""

import graphene
import pytest

import graphanno
from .test_objects import duplicated
from .utils import to_dict


@graphanno.graph_annotations
class Duplicated:
    """Wrapper for the Duplicate class. The name is purposely the same as the name of the model,
    this will cause the name clash"""
    __model__ = duplicated.Duplicated
    __excluded_fields__ = ('to_exclude',)


@graphanno.graph_annotations
class DuplicateUser:
    """Wrapper for DuplicateUser."""
    __model__ = duplicated.DuplicateUser


@graphanno.graph_annotations
class DuplicateUser2:
    """Second example, the annotations order is now different (parent class is annotated first)."""
    __model__ = duplicated.DuplicateUser2


@graphanno.graph_annotations
class Duplicated2:
    """Wrapper for the Duplicate class. The name is purposely the same as the name of the model,
    this will cause the name clash"""
    __model__ = duplicated.Duplicated2
    __excluded_fields__ = ('to_exclude',)


class Query(graphene.ObjectType):
    """Test GraphQL query."""
    user = graphene.Field(DuplicateUser)
    duplicate = graphene.Field(Duplicated)
    user2 = graphene.Field(DuplicateUser2)

    @staticmethod
    def resolve_user(*_):
        """Return the DuplicateUser object instance"""
        # pylint: disable=attribute-defined-outside-init
        data = duplicated.DuplicateUser()
        data.duplicate = Query.resolve_duplicate()
        data.name = 'duplicated_parent'
        return data

    @staticmethod
    def resolve_duplicate(*_):
        """Return the Duplicated object instance"""
        # pylint: disable=attribute-defined-outside-init
        duplicate = duplicated.Duplicated()
        duplicate.name = 'duplicated_child'
        return duplicate

    @staticmethod
    def resolve_user2(*_):
        """Return the DuplicateUser2 object instance"""
        # pylint: disable=attribute-defined-outside-init
        data = duplicated.DuplicateUser2()
        data.duplicate = Query.resolve_duplicate()
        data.name = 'duplicated_parent'
        return data


def test_schema():
    """Test DuplicatedUser content."""
    # pylint: disable=no-member
    assert isinstance(DuplicateUser.name, graphene.String)
    assert isinstance(DuplicateUser.duplicate, graphene.Field)
    assert issubclass(DuplicateUser, graphene.ObjectType)

    assert isinstance(Duplicated.name, graphene.String)
    assert not hasattr(Duplicated, 'to_exclude')
    assert issubclass(Duplicated, graphene.ObjectType)

    assert isinstance(DuplicateUser2.name, graphene.String)
    assert isinstance(DuplicateUser2.duplicate, graphene.Field)
    assert issubclass(DuplicateUser2, graphene.ObjectType)

    assert isinstance(Duplicated2.name, graphene.String)
    assert not hasattr(Duplicated2, 'to_exclude')
    assert issubclass(Duplicated2, graphene.ObjectType)


def test_query():
    """Test graphene query with the generated object."""
    schema = graphene.Schema(query=Query)
    response = schema.execute('{duplicate {name}, user {name, duplicate {name} }, '
                              'user2 {name, duplicate {name} }}')
    assert to_dict(response.data) == {
        'duplicate': {'name': 'duplicated_child'},
        'user': {'name': 'duplicated_parent',
                 'duplicate': {'name': 'duplicated_child'}},
        'user2': {'name': 'duplicated_parent',
                  'duplicate': {'name': 'duplicated_child'}}
    }


def test_name_clash():
    """If another class with the same name will be annotated, the exception will be raised."""
    # pylint: disable=redefined-outer-name,unused-variable
    with pytest.raises(graphanno.SchemaClashError) as excinfo:
        @graphanno.graph_annotations
        class Duplicated:
            """Same name, different class"""
            value: int

    assert excinfo.value.args[0] == 'The schema with name "Duplicated" already exists, ' \
                                    'and bases on another class:\n' \
                                    '	- Current: tests.test_duplicated.Duplicated\n' \
                                    '	- Existing: tests.test_objects.duplicated.Duplicated'
