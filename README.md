# graphanno

Use Python 3.6+ type annotations to generate the graphene `ObjectType` classes.  

[![Build Status](https://travis-ci.com/aklajnert/graphanno.svg?branch=master)](https://travis-ci.com/aklajnert/graphanno)
[![PyPI version](https://badge.fury.io/py/graphanno.svg)](https://badge.fury.io/py/graphanno)

## Installation

You can install the project via `pip` by running:  
```bash
pip install graphanno
```

Installation from source:  
```bash
python setup.py install
```

## Usage

The `@graph_annotations` decorator works only with classes that contains type 
annotations. If there are no type annotations within the decorator target, 
`NoAnnotationsError` exception is raised. Arguments without annotations will
be ignored.

To create the `graphene.ObjectType` object, you can just decorate your class with 
`@graph_annotations`. This will replace your decorated class with the `ObjectType` 
subclass.

```python
import graphene
import graphanno

# the class below...
@graphanno.graph_annotations
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
import graphanno

class Annotated: # this class will be still available later
    value: str
    
# the class below...
@graphanno.graph_annotations
class Graphanno: 
    """
    This class can inherit from graphene.Object type already, 
    but it won't change the @graph_annotations behavior.
    """
    __model__ = Annotated
    
# ... is equivalent to:
class Graphene(graphene.ObjectType):
    value = graphene.String()
```

### Additional parameters

- `__excluded_fields__` (tuple): names of the fields that will be excluded from
schema.
- `__ignore_unsupported__` (bool): do not raise an exception for unsupported annotations. 
Default `False`.

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

