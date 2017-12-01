"""
    tests.test_scripts
    ~~~~~~~~~~~~~~~~~~

    Test script function

    :copyright: (c) 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""
import builtins
import os

import pytest

from create_python_project.scripts import BaseScript
from .conftest import TEST_REPO


def test_base_script_with_path(base_script_content):
    # Test init
    invalid_script_path = 'invalid/script.txt'
    with pytest.raises(AssertionError):
        BaseScript(path=invalid_script_path)

    script_path = 'setup.py'
    base_script = BaseScript(path=script_path)
    builtins.open.assert_any_call(base_script.path, 'r')
    builtins.open().read.assert_called()
    assert base_script.content == base_script_content

    # Test path exploration functions
    assert base_script.path == base_script.abspath
    assert base_script.basename == script_path
    assert base_script.dirname == TEST_REPO
    assert base_script.relpath(TEST_REPO) == script_path

    # Test save
    base_script.save()
    builtins.open.assert_any_call(base_script.abspath, 'w')
    builtins.open().write.assert_any_call(base_script_content)


def test_base_script_without_path(base_script_content):
    # Test init
    base_script = BaseScript()
    assert base_script.path is None
    assert base_script.content is None

    base_script = BaseScript(content=base_script_content)
    assert base_script.content == base_script_content

    # Test path exploration functions
    assert base_script.abspath is None
    assert base_script.basename is None
    assert base_script.dirname is None
    assert base_script.relpath(TEST_REPO) is None

    # Test set_path
    valid_path = 'docs/conf.py'
    base_script.set_path(valid_path)
    assert base_script.path == os.path.join(TEST_REPO, valid_path)

    valid_path = 'docs/test.py'
    base_script.set_path(os.path.join(TEST_REPO, valid_path))
    assert base_script.path == os.path.join(TEST_REPO, valid_path)

    with pytest.raises(AssertionError):
        base_script.set_path(os.path.join(TEST_REPO, 'invalid/test.txt'))
    assert base_script.path == os.path.join(TEST_REPO, valid_path)
