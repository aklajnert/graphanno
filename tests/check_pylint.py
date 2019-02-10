import graphene


class ExampleSchema(graphene.ObjectType):
    """Graphene object that bases on Example class."""
    instance = None

    @classmethod
    def __init_subclass_with_meta__(cls, *args, **kwargs):
        return super().__init_subclass_with_meta__(
            *args, default_resolver=cls._default_fields_resolver, **kwargs)

    @classmethod
    def _default_fields_resolver(cls, attr_name, *_):
        return getattr(cls.instance, attr_name)
