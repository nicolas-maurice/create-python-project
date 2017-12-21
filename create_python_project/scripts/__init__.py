"""
    create_python_project.scripts
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Module that implements class to enable scripts manipulation

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

from .base import BaseScript
from .ini import IniScript
from .init import PyInitScript
from .py import PyScript
from .rst import RSTScript
from .setup import PySetupScript

__all__ = [
    'BaseScript',
    'RSTScript',
    'PyScript',
    'PySetupScript',
    'PyInitScript',
    'IniScript',
]
