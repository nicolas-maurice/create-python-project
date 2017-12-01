"""
    create_python_project
    ~~~~~~~~~~~~~~~~~~~~~

    CLI application to facilitate Python project management

    :copyright: (c) 2017 by Nicolas Maurice.
    :license: BSD, see :ref:`license` for more details.
"""

from .git import RepositoryManager

__version__ = '0.0.0'

__all__ = [
    'RepositoryManager',
]
