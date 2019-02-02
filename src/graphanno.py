"""Main module."""
from datetime import date, datetime, time

import graphene

BASIC_TYPE_MAPPINGS = {
    str: graphene.String,
    int: graphene.Int,
    bool: graphene.Boolean,
    float: graphene.Float,
    date: graphene.Date,
    datetime: graphene.DateTime,
    time: graphene.Time,
}

ADVANCED_TYPE_MAPPINGS = {
    'List': graphene.List
}

UNSUPORTED_TYPES = (list, dict)


class UnsupportedAnnotation(Exception):
    """Raised on unsupported annotation resolve attempt."""


def graph_annotations(cls):
    """Prepare GraphQL schema based on the type annotations."""
    attributes = {}
    target_class = cls.__model__
    ignore_unsupported = getattr(cls, '__ignore_unsupported__', False)

    annotations = dict(**getattr(target_class, '__annotations__', {}))
    annotations.update(getattr(cls, '__annotations__', {}))

    for name, annotation in annotations.items():
        if annotation in UNSUPORTED_TYPES:
            if ignore_unsupported:
                continue
            raise UnsupportedAnnotation(f'The type annotation: {annotation} is not supported.')
        attributes[name] = _get_type_from_annotation(annotation)

    return type(cls.__name__, (graphene.ObjectType,), attributes)


def _get_type_from_annotation(annotation):
    basic_type = BASIC_TYPE_MAPPINGS.get(annotation)
    if basic_type:
        return basic_type()

    if annotation._name == 'List': # pylint: disable=protected-access
        return graphene.List(_get_sub_annotations(annotation))

    return None


def _get_sub_annotations(annotation):
    return tuple(_get_type_from_annotation(sub_annotation) for sub_annotation in annotation.__args__)
