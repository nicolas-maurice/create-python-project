"""
    scripts.base
    ~~~~~~~~~~~~

    Base class for script manipulation

    :copyright: (c) 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import os
from inspect import isclass

from docutils.core import Publisher
from docutils.io import TransformSpec, Input, FileInput, StringInput, NullInput, Output, FileOutput, StringOutput, ErrorOutput
from docutils.nodes import TextElement
from docutils.parsers import Parser
from docutils.readers.standalone import Reader
from docutils.writers import Writer

from ..pyutils import object_with_init_subclass


class TransformSpecDescriptor(object_with_init_subclass):
    """Base class for Input Output descriptors"""

    transform_spec_class = TransformSpec

    def __init__(self):
        self._transform_spec = None

    def __get__(self, instance, owner):
        return self._transform_spec

    def __set__(self, instance, value, *args, **kwargs):
        if isinstance(value, self.transform_spec_class):
            self._transform_spec = value

        else:
            self._transform_spec = self.transform_spec_class(*args, **kwargs)

    def __init_subclass__(cls, **kwargs):
        """This method just terminates the super() chain"""
        transform_spec_class = getattr(cls, "transform_spec_class", None)
        assert transform_spec_class is not None, 'You must provide a transform_spec_class'
        assert isclass(transform_spec_class) and issubclass(transform_spec_class, TransformSpec), \
            'transform_spec_class must be a %s but you provided %s' % (TransformSpec, transform_spec_class)

        super_class = super(cls, cls)
        super_class.__init_subclass_with_transform_spec_class__(transform_spec_class)

    @classmethod
    def __init_subclass_with_transform_spec_class__(cls, transform_spec_class):
        """This method just terminates the super() chain"""


class SourceDescriptor(TransformSpecDescriptor):
    transform_spec_class = Input

    def __set__(self, instance, value, *args, **kwargs):
        if isinstance(value, str):
            if os.path.isfile(value):
                source = FileInput(source_path=os.path.abspath(value))
            else:
                source = StringInput(value)
        else:
            source = NullInput()
        super().__set__(instance, source, *args, **kwargs)

    @classmethod
    def __init_subclass_with_transform_spec_class__(cls, transform_spec_class):
        super().__init_subclass_with_transform_spec_class__(transform_spec_class)
        assert issubclass(transform_spec_class, Input), \
            'transform_spec_class must be a %s but you provided %s' % (Input, transform_spec_class)


class DestinationDescriptor(TransformSpecDescriptor):
    transform_spec_class = Output

    def __set__(self, instance, value, *args, **kwargs):
        if isinstance(value, str):
            destination = FileOutput(destination_path=os.path.abspath(value),
                                     encoding='unicode')
        else:
            destination = StringOutput(encoding='unicode')
        super().__set__(instance, destination, *args, **kwargs)

    @classmethod
    def __init_subclass_with_transform_spec_class__(cls, transform_spec_class):
        super().__init_subclass_with_transform_spec_class__(transform_spec_class)
        assert issubclass(transform_spec_class, Output), \
            'transform_spec_class must be a %s but you provided %s' % (Output, transform_spec_class)


class BaseParser(Parser):
    """Base parser for scripts"""

    def parse(self, inputstring, document):
        document.append(TextElement(text=inputstring))


class BaseWriter(Writer):
    """Base writer for scripts"""

    def translate(self):
        self.output = self.document.astext()


class BaseScript(Publisher):
    """Base class for manipulating scripts"""
    supported_format = ('*',)

    source = SourceDescriptor()
    destination = DestinationDescriptor()

    reader_class = Reader
    writer_class = BaseWriter
    parser_class = BaseParser

    def __init__(self, reader=None, parser=None, writer=None,
                 source=None, destination=None):
        self.document = None
        """The document tree (`docutils.nodes` objects)."""

        self.reader = reader or self.reader_class()
        """A `docutils.readers.Reader` instance."""

        self.parser = parser or self.parser_class()
        """A `docutils.parsers.Parser` instance."""

        self.writer = writer or self.writer_class()
        """A `docutils.writers.Writer` instance."""

        for component in 'reader', 'parser', 'writer':
            assert not isinstance(getattr(self, component), str), (
                'passed string "%s" as "%s" parameter; pass an instance, '
                'or use the "%s_name" parameter instead (in '
                'docutils.core.publish_* convenience functions).'
                % (getattr(self, component), component, component))

        self.source = source
        """The source of input data, a `docutils.io.Input` instance."""

        self.destination = destination
        """The destination for docutils output, a `docutils.io.Output`
        instance."""

        self.get_settings()

        """An object containing Docutils settings as instance attributes.
        Set by `self.process_command_line()` or `self.get_settings()`."""

        self._stderr = ErrorOutput()

    def set_source(self, source=None, source_path=None):
        self.source = source or source_path

    def set_destination(self, destination=None, destination_path=None):
        self.destination = destination or destination_path
