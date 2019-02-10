# graphanno

Use Python 3.6+ type annotations to generate the graphene `ObjectType` classes.

## Installation

You can install the project via `pip` by running:  
```bash
pip install graphanno
```

Installation from source:  
```bash
python setup.py install
```

This module is very simple, you can just copy the [graphanno.py](./graphanno/graphanno.py) file 
into your project (make sure it is visible in your `PYTHONPATH`).

## Usage

The `@graph_annotations` decorator works only with classes that contains type 
annotations. If there are no type annotations within the decorator target, 
`NoAnnotationsError` exception is raised. 

To create the `graphene.ObjectType` object, you can just decorate your class with 
`@graph_annotations`. This will replace your decorated class with the `ObjectType` 
subclass.

```python
import graphene
from graphanno import graph_annotations

# the class below...
@graph_annotations
class Graphanno:
    value: str
    
# ... is equivalent to:
class Graphene(graphene.ObjectType):
    value = graphene.String()
```

If you still need your class with type annotations, set `__model__` variable to annotated
class within the decorated one:

```python
import graphene
from graphanno import graph_annotations

class Annotated: # this class will be still available later
    value: str
    
# the class below...
@graph_annotations
class Graphanno:
    __model__ = Annotated
    
# ... is equivalent to:
class Graphene(graphene.ObjectType):
    value = graphene.String()
```

### Additional parameters

- `__excluded_fields__`: tuple with names of the fields that will be excluded from
schema. 
- `__ignore_unsupported__`: do not raise an exception for unsupported annotations.

## Supported annotations

The class decorated with `@graph_annotations` can use type annotations listed below.

 - str
 - int
 - float
 - bool
 - datetime.datetime
 - datetime.date
 - datetime.time
 - typing.List
 - custom classes with supported type annotations
 
Using unsupported annotations will raise the `UnsupportedAnnotationError` exception. 
To ignore this exception set `__ignore_unsupported__` to `True` in the decorated class.

