"""
    scripts.py
    ~~~~~~~~~~

    Base class for python script manipulation

    :copyright: (c) 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import ast

from .base import BaseScript, BaseReader, BaseParser, BaseWriter
from .content import PyContent
from .info import SingleLineTextInfo
from .rst import RSTScript, RSTVisitor, RSTParser


class PyDocstringVisitor(RSTVisitor):
    """Base class for visiting Python script docstring"""

    def visit_field(self, node):
        field_name, field_body = node.children[0].astext(), node.children[1].children[0].astext()
        if field_name in self.content.info._fields:
            setattr(self.content.info, field_name, SingleLineTextInfo(text=field_body, lineno=node.line - 1))


class PyDocstringParser(RSTParser):
    """Base class for parsing Python Script Docstrings"""

    _rst_visitor_class = PyDocstringVisitor


class PyDocstringScript(RSTScript):
    """Base class for parser python docstring"""

    parser_class = PyDocstringParser


class PyReader(BaseReader):
    """Base class for reading python scripts"""

    content_class = PyContent


class PyParser(BaseParser):
    """Base class for parsing py scripts"""

    def setup_parse(self, input_string):
        super().setup_parse(input_string)
        self.docstring_parser = PyDocstringParser()

        self.ast = ast.parse(input_string)
        self.docstring = ast.get_docstring(self.ast)

    def parse(self, input_string, content):
        super().parse(input_string, content)

        self.parse_docstring(content)
        self.parse_code(content)

        content.set_lines()

    def parse_docstring(self, content):
        if self.docstring is not None:
            content.init_docstring(self.ast.body[0].lineno)
            self.docstring_parser.parse(self.docstring, content.docstring)

    def parse_code(self, content):
        pass


class PyWriter(BaseWriter):
    """Base writer for Python Scripts"""


class PyScript(BaseScript):
    """Base class for manipulating py scripts"""

    supported = (
        '*.py',
    )

    parser_class = PyParser
    reader_class = PyReader
    writer_class = PyWriter
