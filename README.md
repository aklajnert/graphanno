# graphanno

Work in progress. The goal is to leverage Python 3.6+ type annotations to generate
the graphene `ObjectType` classes.

Example usage:
```python
class Basic:
    """Class annotated with the most basic types."""
    number: int = 0
    string: str = ''
    boolean: bool = True
    
# the class below...
@graph_annotations
class BasicSchema:
    __model__ = Basic
    
# ...is equivalent to this:
class BasicSchema(graphene.ObjectType):
    number = graphene.Int()
    string = graphene.String()
    boolean = graphene.Boolean()
```
