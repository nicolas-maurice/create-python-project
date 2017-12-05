"""
    tests.test_scripts
    ~~~~~~~~~~~~~~~~~~

    Test script function

    :copyright: (c) 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import os

import pytest
from docutils.io import TransformSpec, Output, StringOutput, FileOutput, Input, StringInput, FileInput, NullInput

from create_python_project.scripts import BaseScript
from create_python_project.scripts.base import TransformSpecDescriptor, SourceDescriptor, DestinationDescriptor


def _test_invalid_descriptor(descriptor_class, _transform_spec_class):
    with pytest.raises(AssertionError):
        class InvalidDescriptor(descriptor_class):
            transform_spec_class = _transform_spec_class


def test_transform_spec_inheritance():
    class TestDescriptor(TransformSpecDescriptor):
        pass


def test_invalid_descriptors():
    _test_invalid_descriptor(TransformSpecDescriptor, None)
    _test_invalid_descriptor(TransformSpecDescriptor, str)
    _test_invalid_descriptor(TransformSpecDescriptor, 'test')

    _test_invalid_descriptor(SourceDescriptor, Output)

    _test_invalid_descriptor(DestinationDescriptor, Input)


def test_transform_spec_descriptor():
    class TestClass:
        tranform_spec = TransformSpecDescriptor()

    test = TestClass()
    test.tranform_spec = None
    assert isinstance(test.tranform_spec, TransformSpec)


def test_source_descriptor():
    class TestClass:
        source = SourceDescriptor()

    test = TestClass()
    test.source = None
    assert isinstance(test.source, NullInput)


def test_destination_descriptor():
    class TestClass:
        destination = DestinationDescriptor()

    test = TestClass()
    test.destination = 'test'
    assert isinstance(test.destination, FileOutput)


def test_base_script(repo_path, script_content):
    # Test with string input
    base_script = BaseScript(source=script_content)
    assert isinstance(base_script.source, StringInput)
    assert isinstance(base_script.destination, StringOutput)
    assert base_script.publish() == script_content

    # Test with file input
    base_script = BaseScript(source=os.path.join(repo_path, 'setup.py'))
    assert isinstance(base_script.source, FileInput)
    assert isinstance(base_script.destination, StringOutput)

    # Test set_destination and set_source
    base_script.set_destination(None)
    assert isinstance(base_script.destination, StringOutput)
    for dirpath, dirnames, filenames in os.walk(repo_path):
        for filename in filenames:
            base_script.set_source(os.path.join(dirpath, filename))
            assert base_script.source.source_path == os.path.join(dirpath, filename)
            assert base_script.publish() is not None
