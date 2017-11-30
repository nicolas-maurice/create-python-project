"""
    tests.test_import
    ~~~~~~~~~~~~~~~~~

    Test import

    :copyright: (c) 2015 by the Flask Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import create_python_project


def _test_version(module):
    assert hasattr(module, '__version__')


def _test_all(module):
    assert hasattr(module, '__all__')


def test_import():
    _test_version(create_python_project)
    _test_all(create_python_project)
