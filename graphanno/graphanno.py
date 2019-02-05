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

UNSUPORTED_TYPES = (list, dict)


class UnsupportedAnnotationError(Exception):
    """Raised on unsupported annotation resolve attempt."""


class NoAnnotationsError(Exception):
    """Raised when no annotations have been found (or all are excluded)."""


def graph_annotations(cls):
    """Prepare GraphQL schema based on the type annotations."""
    attributes = {}
    target_class = cls.__model__ if hasattr(cls, '__model__') else cls
    ignore_unsupported = getattr(cls, '__ignore_unsupported__', False)
    excluded_keys = getattr(cls, '__excluded_fields__', tuple())

    annotations = dict(**getattr(target_class, '__annotations__', {}))
    annotations.update(getattr(cls, '__annotations__', {}))

    for key in excluded_keys:
        annotations.pop(key)

    if not annotations:
        raise NoAnnotationsError(f'No included annotations for class {cls.__name__}.')

    for name, annotation in annotations.items():
        if annotation in UNSUPORTED_TYPES:
            if ignore_unsupported:
                continue
            raise UnsupportedAnnotationError(f'The type annotation: {annotation} is not supported.')
        type_, args = _get_type_from_annotation(annotation)
        attributes[name] = type_(*args)

    return type(cls.__name__, (graphene.ObjectType,), attributes)


def _get_type_from_annotation(annotation, type_only=False):
    basic_type = BASIC_TYPE_MAPPINGS.get(annotation)
    if basic_type:
        return basic_type if type_only else (basic_type, tuple())

    if str(annotation).startswith('typing.List'):
        return graphene.List, (_get_type_from_annotation(annotation.__args__[0], True),)

    type_ = graph_annotations(annotation)
    return type_ if type_only else (graphene.Field, (type_,))
