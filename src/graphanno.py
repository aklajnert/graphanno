"""Main module."""
import typing
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
    typing.Union: graphene.Union,
    typing.List: graphene.List
}

def graph_annotations(cls):
    """Prepare GrqphQL schema based on the type annotations."""
    attributes = {}
    target_class = cls.__model__

    annotations = dict(**getattr(target_class, '__annotations__', {}))
    annotations.update(getattr(cls, '__annotations__', {}))

    for name, annotation in annotations.items():
        basic_type = BASIC_TYPE_MAPPINGS.get(annotation)
        if basic_type:
            attributes[name] = basic_type()
            continue
    return type(cls.__name__, (graphene.ObjectType,), attributes)
