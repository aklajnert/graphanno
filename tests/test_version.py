"""Test if application version is consistent between module and setup.py"""
import re
from pathlib import Path

import graphanno


def test_version():
    """Verify version consistence."""
    with open(Path(__file__).parents[1] / "setup.py") as setup_file:
        version = re.search(r'version="(\d.\d.\d)",', setup_file.read())

    assert version is not None
    assert version.group(1) == graphanno.__version__
