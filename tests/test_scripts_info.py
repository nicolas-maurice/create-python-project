"""
    tests.test_script_info
    ~~~~~~~~~~~~~~~~~~~~~~

    Test Info implementation functions

    :copyright: (c) 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import pytest

from create_python_project.scripts.info import RSTTitleInfo, TextInfo


def _invalid_modification(instance, attr, value):
    with pytest.raises(Exception):
        setattr(instance, attr, value)


def _valid_modification(instance, attr, value):
    setattr(instance, attr, value)
    assert getattr(instance, attr) == value


def test_text_info():
    text_info = TextInfo()
    _valid_modification(text_info, 'text', 'test')
    _valid_modification(text_info, 'text', '')
    _invalid_modification(text_info, 'text', 4)
    _valid_modification(text_info, 'lineno', 234)
    _invalid_modification(text_info, 'lineno', 3.4)
    _invalid_modification(text_info, 'lineno', '4')


def test_rst_title_info():
    rst_title = RSTTitleInfo()

    _valid_modification(rst_title, 'has_overline', True)
    _invalid_modification(rst_title, 'text', '')
    _invalid_modification(rst_title, 'text', 'multi\nline\ntitle')
    _valid_modification(rst_title, 'symbol', '_')
    _invalid_modification(rst_title, 'symbol', '')
    _invalid_modification(rst_title, 'symbol', '4')
    _invalid_modification(rst_title, 'symbol', '==')
