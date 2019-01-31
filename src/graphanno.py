"""Main module."""
import graphene

BASIC_TYPE_MAPPINGS = {
    str: graphene.String,
    int: graphene.Int,
    bool: graphene.Boolean
}


def graph_annotations(cls):
    """Prepare GrqphQL schema based on the type annotations."""
    attributes = {}
    target_class = cls.__model__
    for name, annotation in target_class.__annotations__.items():
        basic_type = BASIC_TYPE_MAPPINGS.get(annotation)
        if basic_type:
            attributes[name] = basic_type()
            continue
    return type(cls.__name__, (graphene.ObjectType,), attributes)
