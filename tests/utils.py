"""Utility test functions."""
import json


def to_dict(odict):
    """Convert OrderedDict to a regular dictionary"""
    return json.loads(json.dumps(odict))
